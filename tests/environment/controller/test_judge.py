from aurl.environment.controller import judge
from aurl.environment.model import GameState, PlayerAction, PlayerState, TaskState
from aurl.environment import config
import numpy as np


def test_destroy_all_imposter():
    """
    インポスター全滅
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
    players = [
        PlayerState(0, (0, 0), 0),
        PlayerState(0, (0, 0), 1),
        PlayerState(0, (0, 0), 2),
        PlayerState(0, (0, 0), 3),
        PlayerState(1, (0, 0), 4),
    ]
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
    result = judge(state=state)
    assert result == "crew"


def test_destroy_many_crew():
    """
    クルー殺害によるインポスター勝利
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
    players = [
        PlayerState(0, (0, 0), 0),
        PlayerState(0, (0, 0), 1),
        PlayerState(0, (0, 0), 2),
        PlayerState(0, (0, 0), 3),
        PlayerState(1, (0, 0), 4),
    ]
    players[0].dead = True
    players[1].dead = True
    players[2].dead = True
    tasks = [
        TaskState((0, 0), 0)
        for _ in range(config.num_players * config.num_tasks_per_player)
    ]
    state = GameState(
        players=players,
        tasks=tasks,
        game_map=game_map,
    )
    result = judge(state=state)
    assert result == "imposter"


def test_task_completed():
    """
    全タスク完了
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
    players = [
        PlayerState(0, (0, 0), 0),
        PlayerState(0, (0, 0), 1),
        PlayerState(0, (0, 0), 2),
        PlayerState(0, (0, 0), 3),
        PlayerState(1, (0, 0), 4),
    ]
    tasks = [
        TaskState((0, 0), 0)
        for _ in range(config.num_players * config.num_tasks_per_player)
    ]
    for t in tasks:
        t.progress = config.num_task_progress_step
    state = GameState(
        players=players,
        tasks=tasks,
        game_map=game_map,
    )
    result = judge(state=state)
    assert result == "crew"
