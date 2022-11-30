from ..model import TaskState
from typing import List
from .. import config
import numpy as np


def initialize_tasks(game_map: np.ndarray, roles: List[int]) -> List[TaskState]:
    tasks = {}
    mask = game_map == 2
    assert np.count_nonzero(mask) >= config.num_tasks_per_player
    task_position = np.where(mask)
    key = 0
    for i, r in enumerate(roles):
        if r != 0:
            continue
        for j in range(config.num_tasks_per_player):
            position = (task_position[0][j], task_position[1][j])
            task = TaskState(position=position, assignee=i)
            tasks[str(key)] = task
            key += 1
    return [v for v in tasks.values()]
