from aurl.environment.controller import apply_kill
from aurl.environment.model import GameState,PlayerAction,PlayerState,TaskState
from aurl.environment import config
import numpy as np

def test_apply_kill():
    """
    キルが成功
    """
    action = {"0":PlayerAction(0,False,False,[0.0,0.1,0.2,0.3]),
              "1":PlayerAction(0,False,False,[0.2,0.3,0.4,0.5]),
              "2":PlayerAction(0,False,False,[0.4,0.5,0.6,0.7]),
              "3":PlayerAction(0,False,False,[0.6,0.7,0.8,0.9]),
              "4":PlayerAction(0,False,True,[0.8,0.9,0.0,0.1])}
    state = GameState(players=[PlayerState(0,(0,0)) for _ in range(5)], tasks=[TaskState((0,0),0) for _ in range(15)], game_map=np.ndarray((config.map_height,config.map_width)))
    state.players[3].position = (2,2)
    state.players[4].role = 1
    state.players[4].position = (2,2)
    state.players[4].cooltime = 0
    apply_kill(action=action,state=state)
    assert state.players[3].dead
    assert state.players[4].cooltime == config.kill_cooltime
    
def test_crew_wants_kill():
    """
    クルーはキルできない
    """
    action = {"0":PlayerAction(0,False,False,[0.0,0.1,0.2,0.3]),
              "1":PlayerAction(0,False,False,[0.2,0.3,0.4,0.5]),
              "2":PlayerAction(0,False,False,[0.4,0.5,0.6,0.7]),
              "3":PlayerAction(0,False,True,[0.6,0.7,0.8,0.9]),
              "4":PlayerAction(0,False,False,[0.8,0.9,0.0,0.1])}
    state = GameState(players=[PlayerState(0,(0,0)) for _ in range(5)], tasks=[TaskState((0,0),0) for _ in range(15)], game_map=np.ndarray((config.map_height,config.map_width)))
    state.players[3].position = (2,2)
    state.players[3].cooltime = 0
    state.players[4].role = 1
    state.players[4].position = (2,2)
    apply_kill(action=action,state=state)
    assert not state.players[4].dead

def test_deadbody_cannot_kill():
    """
    死んだ後はキルできない
    """
    action = {"0":PlayerAction(0,False,False,[0.0,0.1,0.2,0.3]),
              "1":PlayerAction(0,False,False,[0.2,0.3,0.4,0.5]),
              "2":PlayerAction(0,False,False,[0.4,0.5,0.6,0.7]),
              "3":PlayerAction(0,False,False,[0.6,0.7,0.8,0.9]),
              "4":PlayerAction(0,False,True,[0.8,0.9,0.0,0.1])}
    state = GameState(players=[PlayerState(0,(0,0)) for _ in range(5)], tasks=[TaskState((0,0),0) for _ in range(15)], game_map=np.ndarray((config.map_height,config.map_width)))
    state.players[3].position = (2,2)
    state.players[4].position = (2,2)
    state.players[4].role = 1
    state.players[4].cooltime = 0
    state.players[4].dead = True
    apply_kill(action=action,state=state)
    assert not state.players[3].dead

def test_in_cooltime():
    """
    クールタイム中である
    """
    action = {"0":PlayerAction(0,False,False,[0.0,0.1,0.2,0.3]),
              "1":PlayerAction(0,False,False,[0.2,0.3,0.4,0.5]),
              "2":PlayerAction(0,False,False,[0.4,0.5,0.6,0.7]),
              "3":PlayerAction(0,False,False,[0.6,0.7,0.8,0.9]),
              "4":PlayerAction(0,False,True,[0.8,0.9,0.0,0.1])}
    state = GameState(players=[PlayerState(0,(0,0)) for _ in range(5)], tasks=[TaskState((0,0),0) for _ in range(15)], game_map=np.ndarray((config.map_height,config.map_width)))
    state.players[3].position = (2,2)
    state.players[4].role = 1
    state.players[4].position = (2,2)
    state.players[4].cooltime = 1
    apply_kill(action=action,state=state)
    assert not state.players[3].dead

def test_there_is_no_crew():
    """
    同じマスにいない
    """
    action = {"0":PlayerAction(0,False,False,[0.0,0.1,0.2,0.3]),
              "1":PlayerAction(0,False,False,[0.2,0.3,0.4,0.5]),
              "2":PlayerAction(0,False,False,[0.4,0.5,0.6,0.7]),
              "3":PlayerAction(0,False,False,[0.6,0.7,0.8,0.9]),
              "4":PlayerAction(0,False,True,[0.8,0.9,0.0,0.1])}
    state = GameState(players=[PlayerState(0,(0,0)) for _ in range(5)], tasks=[TaskState((0,0),0) for _ in range(15)], game_map=np.ndarray((config.map_height,config.map_width)))
    state.players[3].position = (2,1)
    state.players[4].role = 1
    state.players[4].position = (2,2)
    state.players[4].cooltime = 0
    apply_kill(action=action,state=state)
    assert not state.players[3].dead

def test_neighbor_is_imposter():
    """
    インポスター同士は殺せない
    """
    action = {"0":PlayerAction(0,False,False,[0.0,0.1,0.2,0.3]),
              "1":PlayerAction(0,False,False,[0.2,0.3,0.4,0.5]),
              "2":PlayerAction(0,False,False,[0.4,0.5,0.6,0.7]),
              "3":PlayerAction(0,False,False,[0.6,0.7,0.8,0.9]),
              "4":PlayerAction(0,False,True,[0.8,0.9,0.0,0.1])}
    state = GameState(players=[PlayerState(0,(0,0)) for _ in range(5)], tasks=[TaskState((0,0),0) for _ in range(15)], game_map=np.ndarray((config.map_height,config.map_width)))
    state.players[3].role = 1
    state.players[3].position = (2,2)
    state.players[4].role = 1
    state.players[4].position = (2,2)
    state.players[4].cooltime = 0
    apply_kill(action=action,state=state)
    assert not state.players[3].dead

def test_already_dead():
    """
    死体はキルできない
    """
    action = {"0":PlayerAction(0,False,False,[0.0,0.1,0.2,0.3]),
              "1":PlayerAction(0,False,False,[0.2,0.3,0.4,0.5]),
              "2":PlayerAction(0,False,False,[0.4,0.5,0.6,0.7]),
              "3":PlayerAction(0,False,False,[0.6,0.7,0.8,0.9]),
              "4":PlayerAction(0,False,True,[0.8,0.9,0.0,0.1])}
    state = GameState(players=[PlayerState(0,(0,0)) for _ in range(5)], tasks=[TaskState((0,0),0) for _ in range(15)], game_map=np.ndarray((config.map_height,config.map_width)))
    state.players[3].position = (2,2)
    state.players[3].dead = True
    state.players[4].role = 1
    state.players[4].position = (2,2)
    state.players[4].cooltime = 0
    apply_kill(action=action,state=state)
    assert not state.players[3].dead
