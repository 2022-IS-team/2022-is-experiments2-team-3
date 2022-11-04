from . import controller
import gym
from gym import spaces
from . import config
import numpy as np
import functools
import copy
from . import model


class AUEnv(gym.Env):
    metadata = {"render_modes": ["rgb_array"]}

    state: model.GameState

    def __init__(self, render_mode=None):
        self.render_mode = render_mode

        player_obs_space = spaces.Dict(
            {
                "dead": spaces.Discrete(2),
                "position": spaces.Box(
                    low=np.array([0.0, 0.0]),
                    high=np.array([config.map_height, config.map_width]),
                    dtype=np.uint8,
                ),
                "surroundings": spaces.Dict(
                    {
                        "here": spaces.Discrete(3),
                        "up": spaces.Discrete(3),
                        "right": spaces.Discrete(3),
                        "down": spaces.Discrete(3),
                        "left": spaces.Discrete(3),
                    }
                ),
                "failed_to_move": spaces.Discrete(2),
                "tasks": spaces.Box(
                    low=0.0,
                    high=1.0,
                    shape=(config.num_tasks_per_player,),
                    dtype=np.float32,
                ),
                "others_pos": spaces.MultiDiscrete(
                    [5 for _ in range(config.num_players - 1)]
                ),
                "others_dead": spaces.MultiDiscrete(
                    [2 for _ in range(config.num_players - 1)]
                ),
                "others_sus": spaces.Box(
                    low=0.0,
                    high=1.0,
                    shape=(config.num_players - 1, config.num_players - 1),
                    dtype=np.float32,
                ),
                "cooltime": spaces.Box(low=0.0, high=1.0, shape=(), dtype=np.float32),
                "report_available": spaces.Discrete(2),
            }
        )

        def dup_players(acc, i):
            acc[str(i)] = copy.deepcopy(player_obs_space)
            return acc

        self.observation_space = spaces.Dict(
            functools.reduce(dup_players, range(config.num_players))
        )

        player_action_space = spaces.Tuple(
            [
                spaces.Discrete(5),  # move
                spaces.Discrete(2),  # report
                spaces.Discrete(2),  # kill
                spaces.Box(low=0.0, high=1.0, shape=(), dtype=np.float32),  # sus
            ]
        )

        def dup_players(acc, i):
            acc[str(i)] = copy.deepcopy(player_action_space)
            return acc

        self.action_space = spaces.Dict(
            functools.reduce(dup_players, range(config.num_players))
        )

    def step(self, action):
        cur_action = controller.convert_action(action)

        controller.update_sus(cur_action, self.state)
        controller.reset_failed_to_move(self.state)

        if self.meeting:
            controller.share_sus(self.state)
            controller.tally_the_votes(self.state)
            judge = controller.judge(self.state)
            observation = controller.state_to_observation(self.state)
            if judge != "continue":
                rewards = controller.calc_reward_on_terminated(self.state)
                info = {"state": self.state, "rewards": rewards}
                return observation, rewards, True, False, info
            else:
                self.state.meeting = False
                rewards = controller.calc_reward_on_meeting(self.state)
                info = {"state": self.state, "rewards": rewards}
                return observation, rewards, False, False, info

        if controller.someone_reported(cur_action, self.state):
            controller.share_dead(self.state)
            controller.share_sus(self.state)
            self.state.meeting = True
            observation = controller.state_to_observation(self.state)
            rewards = controller.calc_reward_on_reported(self.state)
            info = {"state": self.state, "rewards": rewards}
            return observation, rewards, False, False, info

        controller.apply_kill(cur_action, self.state)
        judge = controller.judge(self.state)
        if judge != "continue":
            rewards = controller.calc_reward_on_terminated(self.state)
            info = {"state": self.state, "rewards": rewards}
            return observation, rewards, True, False, info
        
        controller.apply_move(cur_action, self.state)
        controller.update_task_progress(self.state)
        controller.update_cooltimes(self.state)

        observation = controller.state_to_observation(self.state)
        rewards = controller.calc_reward_on_working(self.state)
        info = {"state": self.state, "rewards": rewards}
        return observation, rewards, False, False, info

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        players = controller.initialize_players()
        tasks = controller.initialize_tasks()
        self.state = model.GameState(players=players, tasks=tasks)

        observation = controller.state_to_observation(self.state)
        info = {
            "state": self.state,
            "rewards": [0.0 for _ in range(config.num_players)],
        }
        return observation, info

    def render(self):
        if self.render_mode == "rgb_array":
            return controller.render_state_rgb_array(self.state)
        else:
            return None
