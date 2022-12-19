import aurl.environment
from typing import List, Optional
import numpy as np
import torch as th
import logging
import time
import sys
from stable_baselines3.ppo.ppo import PPO
from stable_baselines3.common.utils import obs_as_tensor, safe_mean
from stable_baselines3.common.buffers import RolloutBuffer
from stable_baselines3.common.callbacks import BaseCallback
from stable_baselines3.common.vec_env import VecEnv
from stable_baselines3.common.type_aliases import GymEnv, MaybeCallback
import gym
from gym.spaces import Box


class MultiAgentLearner(PPO):
    _total_timesteps: int
    _device: th.device
    _last_obs: List[np.ndarray]
    _last_episode_starts: np.ndarray
    _logger: logging.Logger

    def __init__(self, device: th.device):
        super().__init__(
            "MlpPolicy",
            "isteam3/MockAmongUs-v0",
            device=device,
            n_steps=1024,
            verbose=1,
            _init_setup_model=False,
        )
        self.action_space = Box(low=0.0, high=1.0, shape=(7,))
        self.observation_space = Box(low=0.0, high=1.0, shape=(39,))
        self._setup_model()
        # self._logger = logging.getLogger(__name__)
        # handler = logging.StreamHandler()
        # handler.setLevel(logging.DEBUG)
        # self._logger.addHandler(handler)
        # self._logger.setLevel(logging.DEBUG)

    def collect_rollouts(
        self,
        env: VecEnv,
        callback: BaseCallback,
        rollout_buffer: RolloutBuffer,
        n_rollout_steps: int,
    ) -> bool:
        """
        Collect experiences using the current policy and fill a ``RolloutBuffer``.
        The term rollout here refers to the model-free notion and should not
        be used with the concept of rollout used in model-based RL or planning.
        :param env: The training environment
        :param callback: Callback that will be called at each step
            (and at the beginning and end of the rollout)
        :param rollout_buffer: Buffer to fill with rollouts
        :param n_rollout_steps: Number of experiences to collect per environment
        :return: True if function returned with at least `n_rollout_steps`
            collected, False if callback terminated rollout prematurely.
        """
        assert self._last_obs is not None, "No previous observation was provided"
        # Switch to eval mode (this affects batch norm / dropout)
        self.policy.set_training_mode(False)

        n_steps = 0
        rollout_buffer.reset()
        # Sample new weights for the state dependent exploration
        if self.use_sde:
            self.policy.reset_noise(env.num_envs)

        callback.on_rollout_start()

        temp_rollout_buffer_list = [[] for _ in range(5)]

        while n_steps < n_rollout_steps:
            if (
                self.use_sde
                and self.sde_sample_freq > 0
                and n_steps % self.sde_sample_freq == 0
            ):
                # Sample a new noise matrix
                self.policy.reset_noise(env.num_envs)

            actions_list = []
            values_list = []
            log_probs_list = []
            for i in range(5):
                with th.no_grad():
                    # Convert to pytorch tensor or to TensorDict
                    obs_tensor = obs_as_tensor(
                        self._last_obs[:, i * 39 : (i + 1) * 39], self.device
                    )
                    actions, values, log_probs = self.policy(obs_tensor)
                actions = actions.cpu().numpy()

                # Rescale and perform action
                clipped_actions = actions
                # Clip the actions to avoid out of bound error
                if isinstance(self.action_space, gym.spaces.Box):
                    clipped_actions = np.clip(
                        actions, self.action_space.low, self.action_space.high
                    )
                actions_list.append(clipped_actions)
                values_list.append(values)
                log_probs_list.append(log_probs)
            actions = [
                np.concatenate(
                    [actions_of_agent[i] for actions_of_agent in actions_list]
                )
                for i in range(self.n_envs)
            ]

            new_obs, rewards, dones, infos = env.step(actions)

            self.num_timesteps += env.num_envs

            # Give access to local variables
            callback.update_locals(locals())
            if callback.on_step() is False:
                return False

            self._update_info_buffer(infos)
            n_steps += 1

            last_obs_list = [
                [obs[i * 39 : (i + 1) * 39] for obs in self._last_obs] for i in range(5)
            ]
            new_obs_list = [
                [obs[i * 39 : (i + 1) * 39] for obs in new_obs] for i in range(5)
            ]
            rewards_list = [
                [info["rewards"][str(i)] for info in infos] for i in range(5)
            ]

            # if isinstance(self.action_space, gym.spaces.Discrete):
            #     # Reshape in case of discrete action
            #     actions = actions.reshape(-1, 1)

            # Handle timeout by bootstraping with value function
            # see GitHub issue #633
            for idx, done in enumerate(dones):
                if done and infos[idx].get("terminated", True):
                    for i in range(5):
                        terminal_obs = self.policy.obs_to_tensor(new_obs_list[i][idx])[
                            0
                        ]
                        with th.no_grad():
                            terminal_value = self.policy.predict_values(terminal_obs)[0]
                        rewards_list[i][idx] += self.gamma * terminal_value

            for i, (last_obs, actions, rewards, values, log_probs) in enumerate(
                zip(
                    last_obs_list,
                    actions_list,
                    rewards_list,
                    values_list,
                    log_probs_list,
                )
            ):
                temp_rollout_buffer_list[i].append(
                    (
                        last_obs,
                        actions,
                        rewards,
                        self._last_episode_starts,
                        values,
                        log_probs,
                    )
                )
            self._last_obs = new_obs
            self._last_episode_starts = dones

        last_obs_list = [
            [obs[i * 39 : (i + 1) * 39] for obs in self._last_obs] for i in range(5)
        ]
        last_values_and_dones = []
        for new_obs in last_obs_list:
            with th.no_grad():
                # Compute value for the last timestep
                values = self.policy.predict_values(
                    obs_as_tensor(np.array(new_obs), self.device)
                )

            last_values_and_dones.append((values, dones))

        return True, temp_rollout_buffer_list, last_values_and_dones

    def learn(
        self,
        total_timesteps: int,
        callback: MaybeCallback = None,
        log_interval: int = 1,
        eval_env: Optional[GymEnv] = None,
        eval_freq: int = -1,
        n_eval_episodes: int = 5,
        tb_log_name: str = "MAPPO",
        eval_log_path: Optional[str] = None,
        reset_num_timesteps: bool = True,
        progress_bar: bool = False,
    ):
        iteration = 0

        total_timesteps, callback = self._setup_learn(
            total_timesteps,
            eval_env,
            callback,
            eval_freq,
            n_eval_episodes,
            eval_log_path,
            reset_num_timesteps,
            tb_log_name,
            progress_bar,
        )

        callback.on_training_start(locals(), globals())

        while self.num_timesteps < total_timesteps:

            (
                continue_training,
                agents_rollout_buffer_list,
                last_values_and_dones,
            ) = self.collect_rollouts(
                self.env, callback, self.rollout_buffer, n_rollout_steps=self.n_steps
            )

            if continue_training is False:
                break

            agent_index = np.random.randint(0, 5)
            agent_rollout_buffer = agents_rollout_buffer_list[agent_index]
            values, dones = last_values_and_dones[agent_index]
            for (
                last_obs,
                actions,
                rewards,
                last_ep_starts,
                values,
                log_probs,
            ) in agent_rollout_buffer:
                self.rollout_buffer.add(
                    last_obs, actions, rewards, last_ep_starts, values, log_probs
                )

            self.rollout_buffer.compute_returns_and_advantage(
                last_values=values, dones=dones
            )

            callback.on_rollout_end()

            iteration += 1
            self._update_current_progress_remaining(self.num_timesteps, total_timesteps)

            # Display training infos
            if log_interval is not None and iteration % log_interval == 0:
                time_elapsed = max(
                    (time.time_ns() - self.start_time) / 1e9, sys.float_info.epsilon
                )
                fps = int(
                    (self.num_timesteps - self._num_timesteps_at_start) / time_elapsed
                )
                self.logger.record("time/iterations", iteration, exclude="tensorboard")
                if len(self.ep_info_buffer) > 0 and len(self.ep_info_buffer[0]) > 0:
                    self.logger.record(
                        "rollout/ep_rew_mean",
                        safe_mean([ep_info["r"] for ep_info in self.ep_info_buffer]),
                    )
                    self.logger.record(
                        "rollout/ep_len_mean",
                        safe_mean([ep_info["l"] for ep_info in self.ep_info_buffer]),
                    )
                self.logger.record("time/fps", fps)
                self.logger.record(
                    "time/time_elapsed", int(time_elapsed), exclude="tensorboard"
                )
                self.logger.record(
                    "time/total_timesteps", self.num_timesteps, exclude="tensorboard"
                )
                self.logger.dump(step=self.num_timesteps)

            self.train()

        callback.on_training_end()

        return self


def main():
    mal = MultiAgentLearner(device=th.device("cpu"))
    mal.learn(total_timesteps=50000)


if __name__ == "__main__":
    main()
