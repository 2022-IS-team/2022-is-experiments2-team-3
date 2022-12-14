from aurl.environment.controller import initialize_tasks
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
    roles = [0, 0, 0, 1, 0]
    tasks = initialize_tasks(game_map=game_map, roles=roles)
    assert len(tasks) == 4 * config.num_tasks_per_player
    assert tasks[0].assignee == 0
    assert tasks[1].position == (3, 3)
    assert tasks[4].assignee == 1
    assert tasks[12].position == (2, 0)
    assert tasks[12].assignee == 4
