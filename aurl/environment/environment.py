from . import controller
import gym
from . import config
from . import model
from typing import Dict, Union, Any
import numpy as np


class AUEnv(gym.Env):
    metadata = {"render_modes": ["rgb_array"]}

    state: model.GameState

    def __init__(self, render_mode=None):
        self.render_mode = render_mode
        self.observation_space, self.action_space = controller.define_spaces()

    def step(self, action):
        err_msg = f"{action!r} ({type(action)}) invalid"
        assert self.action_space.contains(action), err_msg
        assert self.state is not None, "Call reset before using step method."

        cur_action = controller.convert_action(action)

        controller.update_sus(cur_action, self.state)
        controller.reset_failed_to_move(self.state)

        if self.state.meeting:
            controller.share_sus(self.state)
            controller.tally_the_votes(self.state)
            judge = controller.judge(self.state)
            observation = controller.state_to_observation(self.state)
            if judge != "continue":
                rewards = controller.calc_reward_on_terminated(self.state, judge)
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
            rewards = controller.calc_reward_on_reported(state=self.state)
            info = {"state": self.state, "rewards": rewards}
            return observation, rewards, False, False, info

        controller.apply_kill(cur_action, self.state)
        judge = controller.judge(self.state)
        if judge != "continue":
            observation = controller.state_to_observation(self.state)
            rewards = controller.calc_reward_on_terminated(
                state=self.state, judge=judge
            )
            info = {"state": self.state, "rewards": rewards}
            return observation, rewards, True, False, info

        controller.apply_move(cur_action, self.state)
        controller.update_report_availability(self.state)
        controller.update_task_progress(self.state)
        controller.update_cooltimes(self.state)

        observation = controller.state_to_observation(self.state)
        rewards = controller.calc_reward_on_working(self.state)
        info = {"state": self.state, "rewards": rewards}
        return observation, rewards, False, False, info

    def reset(self, seed=None, options: Union[Dict[str, Any], None] = None):
        super().reset(seed=seed)
        game_map = (
            options["game_map"]
            if options != None and "game_map" in options
            else config.default_game_map
        )
        game_map = np.array(game_map)
        players = controller.initialize_players(game_map=game_map)
        roles = [p.role for p in players]
        tasks = controller.initialize_tasks(game_map=game_map, roles=roles)
        self.state = model.GameState(players=players, tasks=tasks, game_map=game_map)

        observation = controller.state_to_observation(self.state)
        info = {
            "state": self.state,
            "rewards": [0.0 for _ in range(config.num_players)],
        }
        return observation, info

    def render(self):
        if self.render_mode == "rgb_array":
            # return controller.render_state_with_rgb_array(self.state)
            return None
        else:
            return None
