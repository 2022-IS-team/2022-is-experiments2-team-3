import gym
from typing import List, Tuple
import numpy as np
import aurl.environment

params_per_player = 39


class VecEnv:
    _envs: List[gym.Env]
    num_env: int

    def __init__(self, num_env: int):
        self.num_env = num_env
        self._envs = [gym.make("isteam3/MockAmongUs-v0") for _ in range(num_env)]

    def reset(self) -> List[np.ndarray]:
        agent_obs = [[] for _ in range(5)]
        for env in self._envs:
            obs, rewards = env.reset()
            for i in range(5):
                agent_obs[i].append(
                    obs[i * params_per_player : (i + 1) * params_per_player]
                )

        return [np.array(obs) for obs in agent_obs]

    def step(
        self, action_list: List[List[np.ndarray]]
    ) -> Tuple[List[np.ndarray], List[np.ndarray], np.ndarray, np.ndarray]:
        agent_results = [([], []) for _ in range(5)]
        dones_list = []
        terminated_list = []
        assert len(action_list) == len(self._envs)
        for env_idx, (env, agent_action_list) in enumerate(
            zip(self._envs, action_list)
        ):
            actions = np.concatenate(agent_action_list).tolist()
            obs, rewards, terminated, truncated, info = env.step(actions)  # type:ignore
            agent_obs_list = [
                obs[i * params_per_player : (i + 1) * params_per_player]
                for i in range(5)
            ]
            agent_rewards_list = [rewards[str(i)] for i in range(5)]  # type:ignore
            for i in range(5):
                agent_results[i][0].append(agent_obs_list)
                agent_results[i][1].append(agent_rewards_list)
            dones_list.append(terminated or truncated)
            terminated_list.append(terminated)

        obs_list = [np.array(result[0]) for result in agent_results]
        rewards_list = [np.array(result[1]) for result in agent_results]
        dones_list = np.array(dones_list)
        terminated_list = np.array(terminated_list)

        return obs_list, rewards_list, dones_list, terminated_list


# for test
if __name__ == "__main__":
    ve = VecEnv(3)
    obs_list = ve.reset()
    print(len(obs_list), obs_list[0].shape)
    obs_list, rewards_list, dones_list, terminated_list = ve.step(
        [[np.zeros(7) for _ in range(5)] for _ in range(3)]
    )
    print(len(obs_list), obs_list[0].shape)
    print(len(rewards_list), rewards_list[0].shape)
    print(dones_list.shape)
    print(terminated_list.shape)
