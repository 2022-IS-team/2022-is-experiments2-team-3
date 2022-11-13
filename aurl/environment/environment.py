from . import controller
import gym
from . import config
from . import model


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

        if self.meeting:
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
        controller.update_report_availability(self.state)
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
