from .vecenv import VecEnv
from stable_baselines3.ppo.ppo import PPO
from typing import List


class MultiAgentLearner:
    _agents: List[PPO]
    _total_timesteps: int

    def __init__(self, total_timesteps):
        self._agents = [PPO("MlpPolicy", "isteam3/MockAmongUs") for _ in range(5)]
        self._total_timesteps = total_timesteps

    def learn(self):
        envs = VecEnv(3)

        for timestep in range(self._total_timesteps):
            rollout_buffer = self._collect_rollout()

    def _collect_rollout(self):

        pass

    def _train(self):
        pass

    def _register_log(self):
        pass


def main():
    pass
