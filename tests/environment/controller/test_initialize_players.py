from aurl.environment.controller import initialize_players
from aurl.environment.model import GameState, PlayerAction, PlayerState, TaskState
from aurl.environment import config
import numpy as np


def test_1():
    """
    マップに応じてランダムにプレイヤー生成
    """
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
    players = initialize_players(game_map=game_map)
    assert len(players) == config.num_players
    num_imposter = sum([1 if p.role == 1 else 0 for p in players.values()])
    assert num_imposter == config.num_imposter
    assert players["0"].position == (0, 3)
    assert players["1"].position == (0, 4)
    assert players["2"].position == (0, 5)
    assert players["3"].position == (1, 3)
    assert players["4"].position == (1, 4)
