from . import environment
import gym
import time
import shutil
import numpy as np


def main():
    env = gym.make("isteam3/MockAmongUs-v0", render_mode="ansi")

    max_episodes = 100
    max_steps = 500
    # print(type(env.action_space.sample()))
    for episode in range(max_episodes):
        env.reset()
        render(action=None, env=env, episode=episode, step=-1)
        for step in range(max_steps):
            action = env.action_space.sample()
            observation, reward, terminated, truncated, info = env.step(action=action)
            # print(observation, reward, terminated, truncated, info)
            render(action=action, env=env, episode=episode, step=step)

            time.sleep(0.01)

            if terminated or truncated:
                break


def render(action, env, episode, step):
    output_line_height = shutil.get_terminal_size().lines - 1

    env_str = env.render()
    lines = [""]
    lines.append("Episode:%3d -- Step:%3d" % (episode, step))

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
