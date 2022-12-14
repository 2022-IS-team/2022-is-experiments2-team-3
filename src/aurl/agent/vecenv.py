import gym
from typing import List, Tuple
import numpy as np
import aurl.environment


class VecEnv:
    _envs: List[gym.Env]
    _dones: List[bool]
    _num_env: int

    def __init__(self, num_env: int):
        self._num_env = num_env
        self._envs = [gym.make("isteam3/MockAmongUs-v0") for _ in range(num_env)]
        self._dones = [True for _ in range(num_env)]

    def reset(self) -> None:
        for env in self._envs:
            env.reset()
        self._dones = [False for _ in range(self._num_env)]

    def step(self, action_list) -> List[List[Tuple[np.ndarray, float]]]:
        results = []
        assert len(action_list) == len(self._envs)
        for env_idx, (env, agent_action_list, done) in enumerate(
            zip(self._envs, action_list, self._dones)
        ):
            if done:
                results.append(([], []))
                continue
            actions = np.concatenate(agent_action_list).tolist()
            obs, reward, terminated, truncated, info = env.step(actions)
            params_per_player = 39
            agent_obs_list = [
                np.array(obs[i * params_per_player : (i + 1)]) for i in range(5)
            ]
            agent_reward_list = [reward[str(i)] for i in range(5)]  # type:ignore
            results.append((agent_obs_list, agent_reward_list))

            if terminated or truncated:
                self._dones[env_idx] = True
        return results


# for test
if __name__ == "__main__":
    ve = VecEnv(3)
    ve.reset()
    results = ve.step([[np.zeros(7) for _ in range(5)] for _ in range(3)])
    print(results)
