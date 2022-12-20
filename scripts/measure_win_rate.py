from aurl import environment
from aurl.multi_agent_ppo import MultiAgentPPO
import gym
import numpy as np
import torch as th
import os
from datetime import datetime
from tqdm import tqdm
import pandas as pd
from multiprocessing import Pool


def proc(idx):
    print(f"Process {idx:3} | start")
    steps_interval = 20480
    pretrained_root = "experiments/exp1_exp_2022-12-20_01:24:06"
    max_steps = 10000
    iteration = 2
    out_dir = "analytics"

    device = th.device("cuda:0") if th.cuda.is_available() else th.device("cpu")
    mappo = MultiAgentPPO(device=device, tensorboard_log=None)
    env = gym.make("isteam3/MockAmongUs-v0")

    records = []
    model_train_steps = steps_interval * (idx+1)
    pretrained_path = os.path.join(pretrained_root, f"{model_train_steps}steps.pth")
    mappo.set_parameters(pretrained_path)

    for iter_count in range(iteration):
        last_obs = env.reset()
        step = 0
        move_count = [0 for _ in range(5)]
        for _ in range(max_steps):
            actions = mappo(last_obs)
            observations, rewards, done, info = env.step(action=actions)
            last_obs = observations
            rewards = [info["rewards"][str(i)] for i in range(5)]

            for i in range(5):
                if actions[i * 7] >= 0.2 and observations[i * 40 + 9] == 0:
                    move_count[i] += 1

            if done:
                break
            if step == max_steps:
                break

            step += 1

        # 勝敗
        results = [0, 0, 0]  # crew_win, imposter_win, draw
        if step == max_steps:
            results[2] = 1
        else:
            is_p0_win = rewards[0] == 100
            is_p0_crew = observations[0] == 0
            if (is_p0_win and is_p0_crew) or (not is_p0_win and not is_p0_crew):
                results[0] = 1
            else:
                results[1] = 1

        roles = ["crew" if observations[i * 7] == 0 else "imposter" for i in range(5)]
        records.append(
            {
                "model_train_steps": model_train_steps,
                "crew_win": results[0],
                "imposter_win": results[1],
                "draw": results[2],
                "steps": step,
                "move_count_0": move_count[0],
                "move_count_1": move_count[1],
                "move_count_2": move_count[2],
                "move_count_3": move_count[3],
                "move_count_4": move_count[4],
                "role_0": roles[0],
                "role_1": roles[1],
                "role_2": roles[2],
                "role_3": roles[3],
                "role_4": roles[4],
            }
        )
        print(f"Process {idx:3} | iter {iter_count:3} end in {step:8} steps")

    out_path = os.path.join(out_dir, f"rollout_{model_train_steps}steps.csv")
    pd.DataFrame.from_dict(records).to_csv(out_path)
    print(f"Process {idx:3} | complete")


def main():
    steps_count = 10
    
    with Pool(processes=32) as p:
        p.map(func=proc, iterable=list(range(steps_count)))


if __name__ == "__main__":
    main()
