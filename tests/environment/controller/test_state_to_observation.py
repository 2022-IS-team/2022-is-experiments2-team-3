from aurl.environment.controller import state_to_observation
from aurl.environment.model import GameState, PlayerAction, PlayerState, TaskState
from aurl.environment import config
import numpy as np


def test_plain_state():
    """
    初期状態の変換
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
        PlayerState(0, (0, 3), 0),
        PlayerState(0, (0, 4), 1),
        PlayerState(0, (0, 5), 2),
        PlayerState(0, (1, 3), 3),
        PlayerState(1, (1, 4), 4),
    ]
    tasks = []
    for i in range(5):
        for _ in range(4):
            tasks.append(TaskState((0, 0), i))
    state = GameState(
        players=players,
        tasks=tasks,
        game_map=game_map,
    )
    observation = state_to_observation(state=state)
    params_per_player = 11 + config.num_tasks_per_player + (config.num_players - 1) * 3
    assert np.allclose(
        observation[params_per_player*0:params_per_player*1],
        np.array([
            0,0,3/config.map_width, #dead,position
            0,0.2,0,0,0, #surroundings
            0, #failed_to_skip
            0,0,0,0, #tasks
            2/6,0,3/6,0, #others_pos
            0,0,0,0, #others_dead
            0,0,0,0,
            0,0,0,0,
            0,0,0,0,
            0,0,0,0, #others_sus
            0,0 #cooltime,report_available
        ]))  # fmt:skip


def test_surroundings():
    """
    周辺状況の変換
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
        PlayerState(0, (2, 1), 0),
        PlayerState(0, (3, 3), 1),
        PlayerState(0, (1, 4), 2),
        PlayerState(0, (7, 1), 3),
        PlayerState(1, (7, 7), 4),
    ]
    tasks = []
    for i in range(5):
        for _ in range(4):
            tasks.append(TaskState((0, 0), i))
    state = GameState(
        players=players,
        tasks=tasks,
        game_map=game_map,
    )
    observation = state_to_observation(state=state)
    assert observation["0"]["surroundings"]["here"] == 0
    assert observation["0"]["surroundings"]["up"] == 0
    assert observation["0"]["surroundings"]["right"] == 1
    assert observation["0"]["surroundings"]["down"] == 0
    assert observation["0"]["surroundings"]["left"] == 2

    assert observation["1"]["surroundings"]["here"] == 2
    assert observation["1"]["surroundings"]["up"] == 1
    assert observation["1"]["surroundings"]["right"] == 0
    assert observation["1"]["surroundings"]["down"] == 0
    assert observation["1"]["surroundings"]["left"] == 1

    assert observation["2"]["surroundings"]["here"] == 0
    assert observation["2"]["surroundings"]["up"] == 0
    assert observation["2"]["surroundings"]["right"] == 0
    assert observation["2"]["surroundings"]["down"] == 0
    assert observation["2"]["surroundings"]["left"] == 0

    assert observation["3"]["surroundings"]["here"] == 0
    assert observation["3"]["surroundings"]["up"] == 0
    assert observation["3"]["surroundings"]["right"] == 0
    assert observation["3"]["surroundings"]["down"] == 1
    assert observation["3"]["surroundings"]["left"] == 2

    assert observation["4"]["surroundings"]["here"] == 0
    assert observation["4"]["surroundings"]["up"] == 0
    assert observation["4"]["surroundings"]["right"] == 1
    assert observation["4"]["surroundings"]["down"] == 1
    assert observation["4"]["surroundings"]["left"] == 0


def test_others_pos_1():
    """
    他プレイヤーの位置
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
        PlayerState(0, (1, 3), 0),
        PlayerState(0, (1, 4), 1),
        PlayerState(0, (1, 4), 2),
        PlayerState(0, (2, 4), 3),
        PlayerState(1, (7, 7), 4),
    ]
    tasks = []
    for i in range(5):
        for _ in range(4):
            tasks.append(TaskState((0, 0), i))
    state = GameState(
        players=players,
        tasks=tasks,
        game_map=game_map,
    )
    observation = state_to_observation(state=state)
    print(observation)
    assert observation["0"]["others_pos"][0] == 2
    assert observation["0"]["others_pos"][1] == 2
    assert observation["0"]["others_pos"][2] == 5
    assert observation["0"]["others_pos"][3] == 5

    assert observation["1"]["others_pos"][0] == 4
    assert observation["1"]["others_pos"][1] == 0
    assert observation["1"]["others_pos"][2] == 3
    assert observation["1"]["others_pos"][3] == 5

    assert observation["2"]["others_pos"][0] == 4
    assert observation["2"]["others_pos"][1] == 0
    assert observation["2"]["others_pos"][2] == 3
    assert observation["2"]["others_pos"][3] == 5

    assert observation["3"]["others_pos"][0] == 5
    assert observation["3"]["others_pos"][1] == 1
    assert observation["3"]["others_pos"][2] == 1
    assert observation["3"]["others_pos"][3] == 5

    assert observation["4"]["others_pos"][0] == 5
    assert observation["4"]["others_pos"][1] == 5
    assert observation["4"]["others_pos"][2] == 5
    assert observation["4"]["others_pos"][3] == 5


def test_others_pos_2():
    """
    他プレイヤーの位置(死亡含む)
    ついでにreport_availableも検証
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
        PlayerState(0, (2, 3), 0),
        PlayerState(0, (1, 4), 1),
        PlayerState(0, (2, 4), 2),
        PlayerState(0, (2, 4), 3),
        PlayerState(1, (7, 7), 4),
    ]
    players[0].dead = True
    players[0].died_at = (1, 3)
    players[0].reported = True
    players[1].report_available = True
    players[2].dead = True
    players[2].died_at = (1, 4)
    players[2].reported = False
    tasks = []
    for i in range(5):
        for _ in range(4):
            tasks.append(TaskState((0, 0), i))
    state = GameState(
        players=players,
        tasks=tasks,
        game_map=game_map,
    )
    observation = state_to_observation(state=state)
    print(observation)
    assert observation["0"]["others_pos"][0] == 5
    assert observation["0"]["others_pos"][1] == 2
    assert observation["0"]["others_pos"][2] == 2
    assert observation["0"]["others_pos"][3] == 5

    assert observation["1"]["others_pos"][0] == 5
    assert observation["1"]["others_pos"][1] == 0
    assert observation["1"]["others_pos"][2] == 3
    assert observation["1"]["others_pos"][3] == 5
    assert observation["1"]["report_available"] == 1

    assert observation["2"]["others_pos"][0] == 4
    assert observation["2"]["others_pos"][1] == 1
    assert observation["2"]["others_pos"][2] == 0
    assert observation["2"]["others_pos"][3] == 5

    assert observation["3"]["others_pos"][0] == 5
    assert observation["3"]["others_pos"][1] == 1
    assert observation["3"]["others_pos"][2] == 1
    assert observation["3"]["others_pos"][3] == 5

    assert observation["4"]["others_pos"][0] == 5
    assert observation["4"]["others_pos"][1] == 5
    assert observation["4"]["others_pos"][2] == 5
    assert observation["4"]["others_pos"][3] == 5


def test_others_dead():
    """
    他プレイヤー死亡判定
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
        PlayerState(0, (1, 3), 0),
        PlayerState(0, (1, 4), 1),
        PlayerState(0, (1, 4), 2),
        PlayerState(0, (2, 4), 3),
        PlayerState(1, (7, 7), 4),
    ]
    players[0].others_dead = {"1": False, "2": True, "3": True, "4": False}
    tasks = []
    for i in range(5):
        for _ in range(4):
            tasks.append(TaskState((0, 0), i))
    state = GameState(
        players=players,
        tasks=tasks,
        game_map=game_map,
    )
    observation = state_to_observation(state=state)
    print(observation)
    assert observation["0"]["others_dead"][0] == 0
    assert observation["0"]["others_dead"][1] == 1
    assert observation["0"]["others_dead"][2] == 1
    assert observation["0"]["others_dead"][3] == 0


def test_others_sus():
    """
    他プレイヤーsus
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
        PlayerState(0, (1, 3), 0),
        PlayerState(0, (1, 4), 1),
        PlayerState(0, (1, 4), 2),
        PlayerState(0, (2, 4), 3),
        PlayerState(1, (7, 7), 4),
    ]
    players[0].others_sus["1"]["0"] = 1.0
    players[3].others_sus["2"]["4"] = 0.5
    tasks = []
    for i in range(5):
        for _ in range(4):
            tasks.append(TaskState((0, 0), i))
    state = GameState(
        players=players,
        tasks=tasks,
        game_map=game_map,
    )
    observation = state_to_observation(state=state)
    print(observation)
    assert np.allclose(
        observation["0"]["others_sus"],
        np.array([[1.0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]),
    )
    assert np.allclose(
        observation["3"]["others_sus"],
        np.array([[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0.5], [0, 0, 0, 0]]),
    )


def test_others_cooltime():
    """
    クールタイム
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
        PlayerState(0, (1, 3), 0),
        PlayerState(0, (1, 4), 1),
        PlayerState(0, (1, 4), 2),
        PlayerState(0, (2, 4), 3),
        PlayerState(1, (7, 7), 4),
    ]
    players[4].cooltime = 5
    tasks = []
    for i in range(5):
        for _ in range(4):
            tasks.append(TaskState((0, 0), i))
    state = GameState(
        players=players,
        tasks=tasks,
        game_map=game_map,
    )
    observation = state_to_observation(state=state)
    print(observation)
    assert np.allclose(
        observation["4"]["cooltime"],
        np.array([5 / config.kill_cooltime]),
    )
