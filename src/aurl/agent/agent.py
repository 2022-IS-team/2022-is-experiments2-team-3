from .vecenv import VecEnv
from stable_baselines3.ppo.ppo import PPO
from typing import List, Tuple
import numpy as np


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
        RolloutBufferはそれぞれ全ステップ分の(行動、1ステップ前の観測、報酬、価値、log_probs)のタプルのリスト

        エージェントはそれぞれPPOのインスタンスとしてリストself._agentsの中に入っている
        行動の決定はself._agentsのそれぞれのpolicyで行う

        envはenv.step(agent_action_list)で1ステップ進む。返り値はobs_list, reward_list, done
        agent_action_listは各エージェントの行動(ndarray)のリスト
        obs_listは観測(ndarray)のリスト
        reward_listは報酬(float)のリスト
        doneはTrueならゲーム終了
        """
        pass

    def _train(self):
        pass

    def _register_log(self):
        pass


def main():
    pass
