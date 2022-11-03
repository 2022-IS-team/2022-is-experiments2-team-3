from .model import GameState
from . import controller
from gym import Env


class AUEnv:
    def __init__(self):
        players = controller.initialize_players()
        tasks = controller.initialize_tasks()
        self.state = GameState(players=players, tasks=tasks)

    def step(self, action):
        controller.updateSUS(self.state)
        controller.reset_failed_to_move(self.state)

        if self.meeting:
            controller.share_sus(self.state)
            judge = controller.tally_the_votes(self.state)
            observation = controller.state_to_observation(self.state)
            if judge != "continue":
                rewards = controller.calc_reward_on_terminated(self.state)
                return observation, rewards, True, False, self.state
            else:
                self.state.meeting = False
                rewards = controller.calc_reward_on_meeting(self.state)
                return observation, rewards, False, False, self.state

        if controller.someone_reported(action, self.state):
            controller.share_sus(self.state)
            self.state.meeting = True
            observation = controller.state_to_observation(self.state)
            rewards = controller.calc_reward_on_reported(self.state)
            return observation, rewards, False, False, self.state

        controller.apply_kill(action, self.state)
        controller.apply_move(action, self.state)
        controller.update_task_progress(self.state)
        controller.update_cooltimes(self.state)

        observation = controller.state_to_observation(self.state)
        rewards = controller.calc_reward_on_working(self.state)
        return observation, rewards, False, False, self.state

    def reset(self):
        players = controller.initialize_players()
        tasks = controller.initialize_tasks()
        self.state = GameState(players=players, tasks=tasks)

    def render(self):
        if self.render_mode == "rgb_array":
            return controller.render_state_rgb_array(self.state)
        else:
            return None
