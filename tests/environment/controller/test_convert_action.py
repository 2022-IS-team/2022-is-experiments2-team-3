from aurl.environment.controller import convert_action
from aurl.environment.model import GameState, PlayerAction, PlayerState, TaskState
from aurl.environment import config
import numpy as np
from gym.spaces import Space


def test_1():
    input_action = {
        "0": (3, 0, 0, [0.1, 0.2, 0.3, 0.4]),
        "1": (0, 0, 1, [0.1, 0.2, 0.3, 0.4]),
        "2": (0, 1, 0, [0.1, 0.2, 0.3, 0.4]),
        "3": (0, 0, 0, [0.1, 0.2, 0.3, 0.4]),
        "4": (0, 0, 0, [0.3, 0.2, 0.5, 1.0]),
    }
    action = convert_action(input_action)
    assert action["0"].move == 3
    assert action["1"].kill
    assert action["2"].report
    assert action["4"].sus == {"0": 0.3, "1": 0.2, "2": 0.5, "3": 1.0}
