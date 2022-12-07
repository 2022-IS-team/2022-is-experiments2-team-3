from aurl.environment.controller import someone_reported
from aurl.environment.model import GameState, PlayerState, TaskState, PlayerAction
from aurl.environment import config
import numpy as np


def test_someone_reported():
    action = {
        "0": PlayerAction(0, False, False, [0.0, 0.1, 0.2, 0.3]),
        "1": PlayerAction(0, False, False, [0.2, 0.3, 0.4, 0.5]),
        "2": PlayerAction(0, False, False, [0.4, 0.5, 0.6, 0.7]),
        "3": PlayerAction(0, False, False, [0.6, 0.7, 0.8, 0.9]),
        "4": PlayerAction(0, True, False, [0.8, 0.9, 0.0, 0.1]),
    }
    state = GameState(
        players=[PlayerState(0, (0, 0), i) for i in range(5)],
        tasks=[TaskState((0, 0), 0) for _ in range(15)],
        game_map=np.ndarray((config.map_height, config.map_width)),
    )
    state.players[3].dead = True
    state.players[3].reported = False
    state.players[4].report_available = True
    is_reported = someone_reported(action=action, state=state)
    assert state.players[3].reported
    assert is_reported


def test_noone_reported():
    action = {
        "0": PlayerAction(0, False, False, [0.0, 0.1, 0.2, 0.3]),
        "1": PlayerAction(0, False, False, [0.2, 0.3, 0.4, 0.5]),
        "2": PlayerAction(0, False, False, [0.4, 0.5, 0.6, 0.7]),
        "3": PlayerAction(0, False, False, [0.6, 0.7, 0.8, 0.9]),
        "4": PlayerAction(0, False, False, [0.8, 0.9, 0.0, 0.1]),
    }
    state = GameState(
        players=[PlayerState(0, (0, 0), i) for i in range(5)],
        tasks=[TaskState((0, 0), 0) for _ in range(15)],
        game_map=np.ndarray((config.map_height, config.map_width)),
    )
    state.players[3].dead = True
    state.players[3].reported = False
    state.players[4].report_available = True
    is_reported = someone_reported(action=action, state=state)
    assert not is_reported
    assert not state.players[3].reported


def test_report_not_available():
    action = {
        "0": PlayerAction(0, False, False, [0.0, 0.1, 0.2, 0.3]),
        "1": PlayerAction(0, False, False, [0.2, 0.3, 0.4, 0.5]),
        "2": PlayerAction(0, False, False, [0.4, 0.5, 0.6, 0.7]),
        "3": PlayerAction(0, False, False, [0.6, 0.7, 0.8, 0.9]),
        "4": PlayerAction(0, True, False, [0.8, 0.9, 0.0, 0.1]),
    }
    state = GameState(
        players=[PlayerState(0, (0, 0), i) for i in range(5)],
        tasks=[TaskState((0, 0), 0) for _ in range(15)],
        game_map=np.ndarray((config.map_height, config.map_width)),
    )
    state.players[3].dead = True
    state.players[3].reported = False
    state.players[4].report_available = False
    is_reported = someone_reported(action=action, state=state)
    assert not is_reported
    assert not state.players[3].reported


def test_noone_dead():
    action = {
        "0": PlayerAction(0, False, False, [0.0, 0.1, 0.2, 0.3]),
        "1": PlayerAction(0, False, False, [0.2, 0.3, 0.4, 0.5]),
        "2": PlayerAction(0, False, False, [0.4, 0.5, 0.6, 0.7]),
        "3": PlayerAction(0, False, False, [0.6, 0.7, 0.8, 0.9]),
        "4": PlayerAction(0, True, False, [0.8, 0.9, 0.0, 0.1]),
    }
    state = GameState(
        players=[PlayerState(0, (0, 0), i) for i in range(5)],
        tasks=[TaskState((0, 0), 0) for _ in range(15)],
        game_map=np.ndarray((config.map_height, config.map_width)),
    )
    state.players[3].dead = False
    state.players[3].reported = False
    state.players[4].report_available = False
    is_reported = someone_reported(action=action, state=state)
    assert not is_reported
    assert not state.players[3].reported


def test_already_reported():
    action = {
        "0": PlayerAction(0, False, False, [0.0, 0.1, 0.2, 0.3]),
        "1": PlayerAction(0, False, False, [0.2, 0.3, 0.4, 0.5]),
        "2": PlayerAction(0, False, False, [0.4, 0.5, 0.6, 0.7]),
        "3": PlayerAction(0, False, False, [0.6, 0.7, 0.8, 0.9]),
        "4": PlayerAction(0, True, False, [0.8, 0.9, 0.0, 0.1]),
    }
    state = GameState(
        players=[PlayerState(0, (0, 0), i) for i in range(5)],
        tasks=[TaskState((0, 0), 0) for _ in range(15)],
        game_map=np.ndarray((config.map_height, config.map_width)),
    )
    state.players[3].dead = True
    state.players[3].reported = True
    state.players[4].report_available = False
    is_reported = someone_reported(action=action, state=state)
    assert not is_reported
