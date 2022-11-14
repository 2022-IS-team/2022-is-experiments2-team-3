from aurl.environment.controller import update_report_availability
from aurl.environment.model import GameState, PlayerAction, PlayerState, TaskState
from aurl.environment import config
import numpy as np


def test_update_report_availability():
    game_map = np.array(
        [
            [1, 0, 0, 3, 3, 3, 0, 0],
            [1, 0, 1, 3, 3, 0, 1, 0],
            [2, 0, 1, 1, 0, 1, 1, 0],
            [0, 0, 1, 2, 0, 0, 1, 0],
            [0, 0, 1, 0, 1, 0, 1, 0],
            [1, 0, 1, 0, 1, 2, 0, 0],
            [1, 0, 1, 0, 1, 1, 1, 0],
            [2, 0, 0, 0, 0, 0, 0, 0],
        ]
    )
    players = [
        PlayerState(0, (0, 3), 0),
        PlayerState(0, (0, 4), 1),
        PlayerState(0, (0, 5), 2),
        PlayerState(0, (1, 3), 3),
        PlayerState(1, (1, 4), 4),
    ]
    players[2].dead = True
    players[2].died_at = (0, 3)
    players[3].dead = True
    players[3].died_at = (0, 4)
    players[3].reported = True
    players[4].report_available = True
    tasks = []
    for i in range(5):
        for _ in range(4):
            tasks.append(TaskState((0, 0), i))
    state = GameState(
        players=players,
        tasks=tasks,
        game_map=game_map,
    )
    update_report_availability(state=state)
    assert state.players[0].report_available
    assert not state.players[1].report_available
    assert not state.players[4].report_available
