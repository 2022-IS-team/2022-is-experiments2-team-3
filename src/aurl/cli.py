from . import environment
import gym
import time
import shutil
import numpy as np


def main():
    env = gym.make("isteam3/MockAmongUs-v0", render_mode="ansi")

    max_episodes = 100
    max_steps = 500
    for episode in range(max_episodes):
        env.reset()
        render(action=None, env=env, episode=episode, step=-1)
        for step in range(max_steps):
            action = decide_action()
            observation, reward, terminated, truncated, info = env.step(action=action)
            # print(observation, reward, terminated, truncated, info)
            render(action=action, env=env, episode=episode, step=step)

            time.sleep(0.01)

            if terminated or truncated:
                break


def decide_action():
    action = {}
    for i in range(5):
        action[str(i)] = (
            np.random.randint(0, 5),
            np.random.randint(0, 2),
            np.random.randint(0, 2),
            np.random.rand(4).tolist(),
        )
    return action


def render(action, env, episode, step):
    output_line_height = shutil.get_terminal_size().lines - 1

    env_str = env.render()
    lines = [""]
    lines.append("Episode:%3d -- Step:%3d" % (episode, step))

    lines.append("<Action>")
    action_line = ""
    if not action is None:
        for k, a in action.items():
            if a[0] == 0:
                d = ""
            elif a[0] == 1:
                d = "↑"
            elif a[0] == 2:
                d = "→"
            elif a[0] == 3:
                d = "↓"
            elif a[0] == 4:
                d = "←"
            else:
                d = "E"
            action_line += "P%1s:%1s%1s%1s " % (
                k,
                d,
                "R" if a[1] == 1 else "",
                "K" if a[2] == 1 else "",
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
