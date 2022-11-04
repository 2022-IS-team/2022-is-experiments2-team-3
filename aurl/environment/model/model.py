from .. import config
from typing import Tuple, List
import numpy as np


class PlayerState:
    role: int
    dead: bool
    position: Tuple[int, int]
    sus: List[float]
    others_dead: List[bool]
    others_sus: List[List[float]]
    failed_to_move: bool
    cooltime: int

    def __init__(self, role: int, position: Tuple[int, int]):
        assert role == 0 or role == 1
        self.role = role
        self.dead = False
        self.position = position
        self.sus = [0.0 for _ in range(config.num_players - 1)]
        self.others_dead = [False for _ in range(config.num_players - 1)]
        self.others_sus = [
            [0 for _ in range(config.num_players - 1)]
            for _ in range(config.num_players - 1)
        ]
        self.failed_to_move = False
        self.cooltime = 0


class TaskState:
    position: Tuple[int, int]
    assignee: int
    progress: int

    def __init__(self, position: Tuple[int, int], assignee: int):
        self.position = position
        assert assignee < config.num_players
        self.assignee = assignee
        self.progress = 0


class GameState:
    players: List[PlayerState]
    tasks: List[TaskState]
    game_map: np.ndarray
    meeting: bool
    # sabotages: List[bool]

    def __init__(
        self, players: List[PlayerState], tasks: List[TaskState], game_map: np.ndarray
    ):
        self.players = players
        self.tasks = tasks
        assert game_map.shape == (config.map_height, config.map_width)
        self.game_map = game_map
        self.meeting = False
        # self.sabotages = [False, False, False]
