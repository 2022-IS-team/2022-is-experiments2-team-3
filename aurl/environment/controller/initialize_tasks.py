from ..model import TaskState
from typing import Dict
from .. import config
import numpy as np


def initialize_tasks(game_map: np.ndarray) -> Dict[str, TaskState]:
    tasks = {}
    mask = game_map == 2
    assert np.count_nonzero(mask) >= config.num_tasks_per_player
    task_position = np.where(mask)
    for i in range(config.num_players):
        for j in range(config.num_tasks_per_player):
            key = i * config.num_tasks_per_player + j
            position = (task_position[0][j], task_position[1][j])
            task = TaskState(position=position, assignee=i)
            tasks[str(key)] = task
    return tasks
