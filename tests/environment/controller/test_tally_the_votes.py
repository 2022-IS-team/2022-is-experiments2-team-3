from aurl.environment.controller import tally_the_votes
from aurl.environment.model import GameState,PlayerAction,PlayerState,TaskState
from aurl.environment import config
import numpy as np

def test_no_vote_1():
    """
    全員無投票
    """
    state = GameState(players=[PlayerState(0,(0,0)) for _ in range(5)], tasks=[TaskState((0,0),0) for _ in range(15)], game_map=np.ndarray((config.map_height,config.map_width)))
    state.players[0].sus = [0.0,0.1,0.2,0.3]
    state.players[1].sus = [0.0,0.1,0.2,0.3]
    state.players[2].sus = [0.5,0.1,0.2,0.3]
    state.players[3].sus = [0.5,0.7,0.2,0.3]
    state.players[4].sus = [0.5,0.1,0.2,0.3]
    tally_the_votes(state=state)
    assert not state.players[0].dead
    assert not state.players[1].dead
    assert not state.players[2].dead
    assert not state.players[3].dead
    assert not state.players[4].dead


def test_no_vote_2():
    """
    無投票が多数派
    """
    state = GameState(players=[PlayerState(0,(0,0)) for _ in range(5)], tasks=[TaskState((0,0),0) for _ in range(15)], game_map=np.ndarray((config.map_height,config.map_width)))
    state.players[0].sus = [0.0,0.1,0.2,0.3]
    state.players[1].sus = [0.0,0.1,0.2,0.3]
    state.players[2].sus = [0.5,0.1,0.2,0.3]
    state.players[3].sus = [0.5,1.0,0.2,0.3]
    state.players[4].sus = [0.5,0.1,0.2,0.3]
    tally_the_votes(state=state)
    assert not state.players[0].dead
    assert not state.players[1].dead
    assert not state.players[2].dead
    assert not state.players[3].dead
    assert not state.players[4].dead

def test_exile():
    """
    4番へ投票が集まり、追放
    """
    state = GameState(players=[PlayerState(0,(0,0)) for _ in range(5)], tasks=[TaskState((0,0),0) for _ in range(15)], game_map=np.ndarray((config.map_height,config.map_width)))
    state.players[0].sus = [0.0,0.1,0.2,1.0]
    state.players[1].sus = [0.0,0.1,0.2,1.0]
    state.players[2].sus = [0.5,0.1,0.2,1.0]
    state.players[3].sus = [0.5,0.1,0.2,1.0]
    state.players[4].sus = [0.8,0.1,0.2,0.3]
    tally_the_votes(state=state)
    assert not state.players[0].dead
    assert not state.players[1].dead
    assert not state.players[2].dead
    assert not state.players[3].dead
    assert state.players[4].dead

def test_invalid_vote():
    """
    票数が同票となり、無効投票、追放なし
    """
    state = GameState(players=[PlayerState(0,(0,0)) for _ in range(5)], tasks=[TaskState((0,0),0) for _ in range(15)], game_map=np.ndarray((config.map_height,config.map_width)))
    state.players[0].sus = [0.0,0.1,0.2,1.0]
    state.players[1].sus = [0.0,0.1,0.2,1.0]
    state.players[2].sus = [0.5,0.1,0.2,0.1]
    state.players[3].sus = [1.0,0.1,0.2,0.1]
    state.players[4].sus = [1.0,0.1,0.2,0.3]
    tally_the_votes(state=state)
    assert not state.players[0].dead
    assert not state.players[1].dead
    assert not state.players[2].dead
    assert not state.players[3].dead
    assert not state.players[4].dead

def test_vote_to_max_sus():
    """
    sus値の最も多い人へ投票する
    """
    state = GameState(players=[PlayerState(0,(0,0)) for _ in range(5)], tasks=[TaskState((0,0),0) for _ in range(15)], game_map=np.ndarray((config.map_height,config.map_width)))
    state.players[0].sus = [0.0,0.1,0.2,1.0]
    state.players[1].sus = [0.0,0.1,0.2,1.0]
    state.players[2].sus = [0.9,0.1,0.2,1.0]
    state.players[3].sus = [1.0,0.1,0.2,0.1]
    state.players[4].sus = [1.0,0.1,0.2,0.3]
    tally_the_votes(state=state)
    assert not state.players[0].dead
    assert not state.players[1].dead
    assert not state.players[2].dead
    assert not state.players[3].dead
    assert state.players[4].dead
