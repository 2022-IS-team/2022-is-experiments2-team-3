from aurl.environment.controller import share_sus
from aurl.environment.model import GameState, PlayerAction, PlayerState, TaskState
from aurl.environment import config
import numpy as np


def test_share_sus():
    state = GameState(
        players=[PlayerState(0, (0, 0), i) for i in range(5)],
        tasks=[TaskState((0, 0), 0) for _ in range(15)],
        game_map=np.ndarray((config.map_height, config.map_width)),
    )
    state.players[0].sus = {"1": 0.0, "2": 0.1, "3": 0.2, "4": 1.0}
    state.players[1].sus = {"0": 0.0, "2": 0.1, "3": 0.3, "4": 1.0}
    state.players[2].sus = {"0": 0.9, "1": 0.1, "3": 0.4, "4": 1.0}
    state.players[3].sus = {"0": 1.0, "1": 0.1, "2": 0.2, "4": 0.1}
    state.players[4].sus = {"0": 1.0, "1": 0.1, "2": 0.2, "3": 0.3}
    share_sus(state=state)
    print(state.players[0].others_sus)
    assert state.players[0].others_sus == {
        "1": {"0": 0.0, "2": 0.1, "3": 0.3, "4": 1.0},
        "2": {"0": 0.9, "1": 0.1, "3": 0.4, "4": 1.0},
        "3": {"0": 1.0, "1": 0.1, "2": 0.2, "4": 0.1},
        "4": {"0": 1.0, "1": 0.1, "2": 0.2, "3": 0.3},
    }
    assert state.players[1].others_sus == {
        "0": {"1": 0.0, "2": 0.1, "3": 0.2, "4": 1.0},
        "2": {"0": 0.9, "1": 0.1, "3": 0.4, "4": 1.0},
        "3": {"0": 1.0, "1": 0.1, "2": 0.2, "4": 0.1},
        "4": {"0": 1.0, "1": 0.1, "2": 0.2, "3": 0.3},
    }
    assert state.players[2].others_sus == {
        "0": {"1": 0.0, "2": 0.1, "3": 0.2, "4": 1.0},
        "1": {"0": 0.0, "2": 0.1, "3": 0.3, "4": 1.0},
        "3": {"0": 1.0, "1": 0.1, "2": 0.2, "4": 0.1},
        "4": {"0": 1.0, "1": 0.1, "2": 0.2, "3": 0.3},
    }
    assert state.players[3].others_sus == {
        "0": {"1": 0.0, "2": 0.1, "3": 0.2, "4": 1.0},
        "1": {"0": 0.0, "2": 0.1, "3": 0.3, "4": 1.0},
        "2": {"0": 0.9, "1": 0.1, "3": 0.4, "4": 1.0},
        "4": {"0": 1.0, "1": 0.1, "2": 0.2, "3": 0.3},
    }
    assert state.players[4].others_sus == {
        "0": {"1": 0.0, "2": 0.1, "3": 0.2, "4": 1.0},
        "1": {"0": 0.0, "2": 0.1, "3": 0.3, "4": 1.0},
        "2": {"0": 0.9, "1": 0.1, "3": 0.4, "4": 1.0},
        "3": {"0": 1.0, "1": 0.1, "2": 0.2, "4": 0.1},
    }
