from .vecenv import VecEnv
from stable_baselines3.ppo.ppo import PPO
from stable_baselines3.common.utils import obs_as_tensor, safe_mean
from typing import List, Tuple
import numpy as np

import gym
import torch as th


class MultiAgentLearner:
    _agents: List[PPO]
    _total_timesteps: int
    _rollout_buffers: List[List[Tuple[np.ndarray, float]]]

    def __init__(self, total_timesteps):
        self._agents = [PPO("MlpPolicy", "isteam3/MockAmongUs") for _ in range(5)]
        self._total_timesteps = total_timesteps
        self._rollout_buffers = [[] for _ in range(5)]

    def learn(self):
        envs = VecEnv(3)

        for timestep in range(self._total_timesteps):
            self._collect_rollout(envs)

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
        last_obs = None
        self.policy.set_training_mode(False)

        n_steps = 0
        self._rollout_buffers = []

        while n_steps < 2048:
            actions_list = []
            clipped_actions_list = []
            values_list = []
            log_probs_list = []

            for i in range(5):
                with th.no_grad():
                    obs_tensor = obs_as_tensor(self.last_obs, self.device)
                    actions, values, log_probs = obs_tensor
                actions_list[i] = actions.cpu().numpy()
                log_probs_list[i] = log_probs

                clipped_actions = actions
                if isinstance(self.action_space, gym.spaces.Box):
                    clipped_actions_list[i] = np.clip(actions, self.action_space.low, self.action_space.high)

            new_obs, rewards, dones, infos = env.step(actions_list)

            self._update_info_buffer(infos)

            n_steps += 1

            # if isinstance(self.action_space, gym.space.Discrete):
            #     actions = actions.reshape(-1,1)

            #infos未定義?
            for i in range(5):
                for idx, done in enumerate(dones):
                    if(
                        done
                        and infos[idx].get("terminal_observation") is not None
                        and infos[idx].get("TimeLimit.truncated", False)
                    ):
                        terminal_obs = self.policy.obs_tensor(infos[idx]["terminal_observation"])[0]
                        with th.no_grad():
                            terminal_value = self.policy.predict_values(terminal_obs)[0]
                        rewards[i][idx] += self.gamma * terminal_value
            
            #_last_episode_starts未実装
            for i in range(5):
                self._rollout_buffers[i].add(last_obs[i], actions_list[i], rewards[i], self._last_episode_starts, values[i], log_probs_list[i])
                last_obs[i] = new_obs[i]

            with th.no_grad():
                for i in range(5):
                    values[i] = self.policy.predict_values(obs_as_tensor(new_obs[i], self.device))

            for i in range(5):
                self._rollout_buffers.compute_returns_and_advantage(last_values=values[i], dones=dones)

        pass

    def _train(self):
        pass

    def _register_log(self):
        pass


def main():
    pass
