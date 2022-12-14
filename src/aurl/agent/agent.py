from aurl.agent.vecenv import VecEnv
from stable_baselines3.ppo.ppo import PPO
from stable_baselines3.common.utils import obs_as_tensor
from typing import List
import numpy as np
import torch as th
import logging


class MultiAgentLearner:
    _agents: List[PPO]
    _total_timesteps: int
    _device: th.device
    _last_obs: List[np.ndarray]
    _last_episode_starts: np.ndarray
    _logger: logging.Logger

    def __init__(self, total_timesteps, device="cpu"):
        self._agents = [PPO("MlpPolicy", "isteam3/MockAmongUs") for _ in range(5)]
        self._total_timesteps = total_timesteps
        self._device = th.device(device)
        self._logger = logging.getLogger(__name__)
        handler = logging.StreamHandler()
        handler.setLevel(logging.DEBUG)
        self._logger.addHandler(handler)
        self._logger.setLevel(logging.DEBUG)

    def learn(self):
        self._logger.info("initializing environments")
        envs = VecEnv(3)

        self._logger.info("setting up agents for learning")
        for agent in self._agents:
            agent._setup_learn(self._total_timesteps, None)

        self._logger.info("setting up learner for learning")
        self._setup_learn(envs)

        self._logger.info("start learning")
        for timestep in range(self._total_timesteps):
            self._collect_rollout(envs)
            self._register_log()
            self._train()

        self._logger.info("finish learning")

    def _setup_learn(self, envs: VecEnv):
        self._last_obs = envs.reset()
        self._last_episode_starts = np.ones(envs.num_env)

    def _collect_rollout(self, env: VecEnv) -> None:
        """
        環境envをゲームが終わるまで回して、その間の各エージェントの行動とその結果環境から返された観測、報酬、価値(value)、log_probsを
        self._rollout_buffersにすべて格納する
        self._rollout_buffersは各エージェントのRolloutBufferのリスト
        RolloutBufferはそれぞれ全ステップ分の(行動、1ステップ前の観測、報酬、_last_episode_starts、価値、log_probs)のタプルのリスト

        エージェントはそれぞれPPOのインスタンスとしてリストself._agentsの中に入っている
        行動の決定はself._agentsのそれぞれのpolicyで行う

        envはenv.step(agent_action_list)で1ステップ進む。返り値はobs_list, reward_list, done
        agent_action_listは各エージェントの行動(ndarray)のリスト
        obs_listは観測(ndarray)のリスト
        reward_listは報酬(float)のリスト
        doneはTrueならゲーム終了
        """
        last_episode_starts = None
        for agent in self._agents:
            agent.policy.set_training_mode(False)

        n_steps = 0
        agent_new_obs = []

        while n_steps < 2048:
            agent_actions = []
            agent_values = []
            agent_log_probs = []

            for i, (agent, obs) in enumerate(zip(self._agents, self._last_obs)):
                with th.no_grad():
                    obs_tensor = obs_as_tensor(obs, self._device)
                    actions, values, log_probs = agent.policy(obs_as_tensor)
                actions = actions.cpu().numpy()
                clipped_actions = np.clip(actions, 0, 1)
                agent_actions.append(clipped_actions)
                agent_values.append(values)
                agent_log_probs.append(log_probs)

            agent_new_obs, agent_rewards, dones, terminated_list = env.step(
                agent_actions
            )

            n_steps += 1

            for i, terminated in enumerate(terminated_list):
                if not terminated:
                    continue
                for j, (agent, agent_obs) in enumerate(
                    zip(self._agents, agent_new_obs)
                ):
                    terminal_obs = agent.policy.obs_to_tensor(agent_obs[i])
                    with th.no_grad():
                        terminal_value = agent.policy.predict_values(terminal_obs)[0]  # type: ignore
                    agent_rewards[j][i] += agent.gamma * terminal_value

            for agent, obs, actions, rewards, episode_starts, values, log_probs in zip(
                self._agents,
                self._last_obs,
                agent_actions,
                agent_rewards,
                self._last_episode_starts,
                agent_values,
                agent_log_probs,
            ):
                agent.rollout_buffer.add(
                    obs,
                    actions,
                    rewards,
                    episode_starts,
                    values,
                    log_probs,
                )

            self._last_obs = agent_new_obs
            self._last_episode_starts = dones

        for agent, obs in zip(self._agents, self._last_obs):
            with th.no_grad():
                values = agent.policy.predict_values(
                    obs_as_tensor(obs, self._device)
                )  # type:ignore

            agent.rollout_buffer.compute_returns_and_advantage(  # type:ignore
                last_values=values, dones=self._last_episode_starts
            )

    def _train(self):
        for agent in self._agents:
            agent.train()

    def _register_log(self):
        pass


def main():
    mal = MultiAgentLearner(total_timesteps=5000)
    mal.learn()


if __name__ == "__main__":
    main()
