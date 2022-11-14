from aurl.environment.controller import reset_failed_to_move
from aurl.environment.model import GameState, PlayerState, TaskState
from aurl.environment import config
import numpy as np


def test_reset_failed_to_move():
    state = GameState(
        players=[PlayerState(0, (0, 0), i) for i in range(5)],
        tasks=[TaskState((0, 0), 0) for _ in range(15)],
        game_map=np.ndarray((config.map_height, config.map_width)),
    )
    state.players[0].failed_to_move = True
    state.players[3].failed_to_move = True
    state.players[4].failed_to_move = True
    reset_failed_to_move(state=state)
    assert not state.players[0].failed_to_move
    assert not state.players[1].failed_to_move
    assert not state.players[2].failed_to_move
    assert not state.players[3].failed_to_move
    assert not state.players[4].failed_to_move
