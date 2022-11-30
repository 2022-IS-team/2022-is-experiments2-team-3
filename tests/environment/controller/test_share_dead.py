from aurl.environment.controller import share_dead
from aurl.environment.model import GameState, PlayerAction, PlayerState, TaskState
from aurl.environment import config
import numpy as np


def test_share_dead():
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
        PlayerState(0, (0, 0), 0),
        PlayerState(0, (0, 0), 1),
        PlayerState(0, (0, 0), 2),
        PlayerState(0, (0, 0), 3),
        PlayerState(1, (0, 0), 4),
    ]
    players[0].dead = True
    players[2].dead = True
    players[4].dead = True
    tasks = [
        TaskState((0, 0), 0)
        for _ in range(config.num_players * config.num_tasks_per_player)
    ]
    state = GameState(
        players=players,
        tasks=tasks,
        game_map=game_map,
    )
    share_dead(state=state)
    assert state.players[0].others_dead["2"]
    assert state.players[1].others_dead["4"]
    assert not state.players[3].others_dead["1"]
