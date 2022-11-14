from aurl.environment.controller import apply_move
from aurl.environment.model import GameState,PlayerAction,PlayerState,TaskState
from aurl.environment import config
import numpy as np

def test_noone_moved():
    """
    移動なし
    """
    action = {"0":PlayerAction(0,False,False,[0.0,0.1,0.2,0.3]),
              "1":PlayerAction(0,False,False,[0.2,0.3,0.4,0.5]),
              "2":PlayerAction(0,False,False,[0.4,0.5,0.6,0.7]),
              "3":PlayerAction(0,False,False,[0.6,0.7,0.8,0.9]),
              "4":PlayerAction(0,False,False,[0.8,0.9,0.0,0.1])}
    game_map = np.array([
        [1,1,1,1,1,1,1,1],
        [1,0,0,0,0,0,0,1],
        [1,0,1,1,0,1,0,1],
        [1,0,1,0,0,0,0,1],
        [1,0,1,0,1,1,0,1],
        [1,0,1,0,1,1,0,1],
        [1,0,0,0,0,0,0,1],
        [1,1,1,1,1,1,1,1],
    ])
    positions = [(1,1),(2,1),(2,4),(4,3),(6,6)]
    state = GameState(players=[PlayerState(0,p,i) for i,p in enumerate(positions)], tasks=[TaskState((0,0),0) for _ in range(15)], game_map=game_map)
    apply_move(action=action,state=state)
    assert state.players[0].position == (1,1)
    assert state.players[1].position == (2,1)
    assert state.players[2].position == (2,4)
    assert state.players[3].position == (4,3)
    assert state.players[4].position == (6,6)
    
def test_everybody_moved():
    """
    全員移動
    """
    action = {"0":PlayerAction(2,False,False,[0.0,0.1,0.2,0.3]),
              "1":PlayerAction(3,False,False,[0.2,0.3,0.4,0.5]),
              "2":PlayerAction(1,False,False,[0.4,0.5,0.6,0.7]),
              "3":PlayerAction(3,False,False,[0.6,0.7,0.8,0.9]),
              "4":PlayerAction(4,False,False,[0.8,0.9,0.0,0.1])}
    game_map = np.array([
        [1,1,1,1,1,1,1,1],
        [1,0,0,0,0,0,0,1],
        [1,0,1,1,0,1,0,1],
        [1,0,1,0,0,0,0,1],
        [1,0,1,0,1,1,0,1],
        [1,0,1,0,1,1,0,1],
        [1,0,0,0,0,0,0,1],
        [1,1,1,1,1,1,1,1],
    ])
    positions = [(1,1),(2,1),(2,4),(4,3),(6,6)]
    state = GameState(players=[PlayerState(0,p,i) for i,p in enumerate(positions)], tasks=[TaskState((0,0),0) for _ in range(15)], game_map=game_map)
    apply_move(action=action,state=state)
    assert state.players[0].position == (1,2)
    assert state.players[1].position == (3,1)
    assert state.players[2].position == (1,4)
    assert state.players[3].position == (5,3)
    assert state.players[4].position == (6,5)
    
def test_collide_with_wall():
    """
    移動不可マスにより移動失敗
    """
    action = {"0":PlayerAction(1,False,False,[0.0,0.1,0.2,0.3]),
              "1":PlayerAction(2,False,False,[0.2,0.3,0.4,0.5]),
              "2":PlayerAction(1,False,False,[0.4,0.5,0.6,0.7]),
              "3":PlayerAction(3,False,False,[0.6,0.7,0.8,0.9]),
              "4":PlayerAction(4,False,False,[0.8,0.9,0.0,0.1])}
    game_map = np.array([
        [1,1,1,1,1,1,1,1],
        [1,0,0,0,0,0,0,1],
        [1,0,1,1,0,1,0,1],
        [1,0,1,0,0,0,0,1],
        [1,0,1,0,1,1,0,1],
        [1,0,1,0,1,1,0,1],
        [1,0,0,0,0,0,0,1],
        [1,1,1,1,1,1,1,1],
    ])
    positions = [(1,1),(2,1),(2,4),(4,3),(6,6)]
    state = GameState(players=[PlayerState(0,p,i) for i,p in enumerate(positions)], tasks=[TaskState((0,0),0) for _ in range(15)], game_map=game_map)
    apply_move(action=action,state=state)
    assert state.players[0].position == (1,1)
    assert state.players[0].failed_to_move
    assert state.players[1].position == (2,1)
    assert state.players[1].failed_to_move
    assert state.players[2].position == (1,4)
    assert not state.players[2].failed_to_move
    
    
def test_goto_outside():
    """
    場外へ出ようとして移動失敗
    """
    action = {"0":PlayerAction(4,False,False,[0.0,0.1,0.2,0.3]),
              "1":PlayerAction(1,False,False,[0.2,0.3,0.4,0.5]),
              "2":PlayerAction(2,False,False,[0.4,0.5,0.6,0.7]),
              "3":PlayerAction(3,False,False,[0.6,0.7,0.8,0.9]),
              "4":PlayerAction(3,False,False,[0.8,0.9,0.0,0.1])}
    game_map = np.array([
        [0,0,1,1,1,1,1,1],
        [1,0,0,0,0,0,0,0],
        [1,0,1,1,0,1,0,1],
        [1,0,1,0,0,0,0,1],
        [1,0,1,0,1,1,0,1],
        [1,0,1,0,1,1,0,1],
        [1,0,0,0,0,0,0,1],
        [1,1,1,1,1,1,0,1],
    ])
    positions = [(0,0),(0,1),(1,7),(4,3),(7,6)]
    state = GameState(players=[PlayerState(0,p,i) for i,p in enumerate(positions)], tasks=[TaskState((0,0),0) for _ in range(15)], game_map=game_map)
    apply_move(action=action,state=state)
    assert state.players[0].position == (0,0)
    assert state.players[0].failed_to_move
    assert state.players[1].position == (0,1)
    assert state.players[1].failed_to_move
    assert state.players[2].position == (1,7)
    assert state.players[2].failed_to_move
    assert state.players[3].position == (5,3)
    assert not state.players[3].failed_to_move
    assert state.players[4].position == (7,6)
    assert state.players[4].failed_to_move
    
    