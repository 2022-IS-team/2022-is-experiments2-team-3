from . import environment
import gym
import time
import shutil
import numpy as np
from .multi_agent_ppo import MultiAgentPPO
import torch as th
import argparse
import os
from datetime import datetime
import pickle

parser = argparse.ArgumentParser()
parser.add_argument("--total_timesteps", default=2048 * 100)
parser.add_argument("--save_interval", default=10)
parser.add_argument("--exp_path", default=".")
parser.add_argument("--pretrained_path", default=None)
parser.add_argument("--skip_learning", default=False)
parser.add_argument("--game_max_steps", default=20000)
parser.add_argument("--continue_learning", default=False)


def main():
    args = parser.parse_args()

    exp_name = datetime.now().strftime("exp_%Y-%m-%d_%H:%M:%S")
    exp_path = os.path.join(args.exp_path, exp_name)
    save_path = exp_path
    log_path = os.path.join(exp_path, "logs")
    game_record_path = os.path.join(exp_path, "game_records")
    os.makedirs(log_path)
    os.makedirs(game_record_path)

    device = th.device("cuda:0") if th.cuda.is_available() else th.device("cpu")
    mappo = MultiAgentPPO(device=device, tensorboard_log=log_path)
    if not args.pretrained_path is None:
        mappo.set_parameters(args.pretrained_path)
    if not args.skip_learning:
        mappo.learn(
            total_timesteps=int(args.total_timesteps),
            save_interval=int(args.save_interval),
            save_path=save_path,
        )
        mappo.save(os.path.join(save_path, "final.zip"))

    record_name = f"{'pretrained' if not args.pretrained_path is None else ''}_{args.total_timesteps}steps"
    record_metadata_path = os.path.join(game_record_path, record_name + "_metadata.txt")
    metadata_txt = [
        f"total_timesteps: {args.total_timesteps}\n",
        f"save_interval: {args.save_interval}\n",
        f"exp_path: {args.exp_path}\n",
        f"pretrained_path: {args.pretrained_path}\n",
        f"skip_learning: {args.skip_learning}\n",
        f"game_max_steps: {args.game_max_steps}\n",
        f"trained_file: {os.path.join(save_path,'final.pth') if not args.skip_learning else args.pretrained_path}\n",
    ]
    with open(record_metadata_path, "w") as f:
        f.writelines(metadata_txt)

    records = rollout(
        mappo,
        max_steps=int(args.game_max_steps),
    )
    pickle_path = os.path.join(game_record_path, record_name + ".pickle")
    with open(pickle_path, "wb") as f:
        pickle.dump(records, f)


def rollout(model: MultiAgentPPO, max_steps):
    env = gym.make("isteam3/MockAmongUs-v0")
    records = []

    last_obs = env.reset()
    render(action=None, env=env, step=-1)
    records.append({"step": -1, "observation": last_obs})

    step = 0
    while True:
        actions = model(last_obs)
        
        observations, rewards, done, info = env.step(action=actions)
        last_obs = observations

        render(action=actions, env=env, step=step)
        records.append(
            {
                "step": step,
                "actions": actions,
                "observations": observations,
                "rewards": rewards,
                "done": done,
                "info": info,
            }
        )
        time.sleep(0.001)

        if done:
            break
        if step == max_steps:
            break

        step += 1
    return records


def render(action, env, step):
    output_line_height = shutil.get_terminal_size().lines - 1

    env_str = env.render(mode="ansi")
    lines = [""]
    lines.append("Step:%3d" % (step,))

    lines.append("<Action>")
    action_line = ""
    if not action is None:
        params_per_player = 7
        for i in range(5):
            if action[params_per_player * i] < 1 / 5:
                d = ""
            elif action[params_per_player * i] < 2 / 5:
                d = "↑"
            elif action[params_per_player * i] < 3 / 5:
                d = "→"
            elif action[params_per_player * i] < 4 / 5:
                d = "↓"
            elif action[params_per_player * i] <= 1:
                d = "←"
            else:
                d = "E"
            action_line += "P%1s:%1s%1s%1s " % (
                str(i),
                d,
                "R"
                if action[params_per_player * i + 1]
                >= environment.config.act_threshould
                else "",
                "K"
                if action[params_per_player * i + 2]
                >= environment.config.act_threshould
                else "",
            )
    lines.append(action_line)

    lines += env_str.splitlines()
    output = ""
    for i in range(output_line_height):
        output += "\033[2K\033[A"
    for i in range(output_line_height):
        if i < len(lines):
            output += lines[i] + "\n"
        else:
            output += "\n"
    output = output.rstrip()
    print(output, end="")
