from aurl.environment.controller import update_task_progress
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
        PlayerState(0, (2, 0), 0),
        PlayerState(0, (3, 3), 1),
        PlayerState(0, (0, 5), 2),
        PlayerState(0, (1, 3), 3),
        PlayerState(1, (1, 4), 4),
    ]
    tasks = []
    for i in range(4):
        for pos in [(2, 0), (3, 3), (5, 5), (7, 0)]:
            tasks.append(TaskState(pos, i))
    tasks[1].progress = 5
    tasks[2].progress = config.num_task_progress_step
    tasks[5].progress = config.num_task_progress_step
    state = GameState(
        players=players,
        tasks=tasks,
        game_map=game_map,
    )
    update_task_progress(state=state)
    assert state.tasks[0].progress == 1
    assert state.tasks[1].progress == 0
    assert state.tasks[2].progress == config.num_task_progress_step
    assert state.tasks[5].progress == config.num_task_progress_step
