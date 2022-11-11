from aurl.environment.controller import update_sus
from aurl.environment.model import GameState,PlayerAction,PlayerState,TaskState
from aurl.environment import config
import numpy as np

def test_update_sus():
    action = {"0":PlayerAction(0,False,False,[0.0,0.1,0.2,0.3]),
              "1":PlayerAction(0,False,False,[0.2,0.3,0.4,0.5]),
              "2":PlayerAction(0,False,False,[0.4,0.5,0.6,0.7]),
              "3":PlayerAction(0,False,False,[0.6,0.7,0.8,0.9]),
              "4":PlayerAction(0,False,False,[0.8,0.9,0.0,0.1])}
    state = GameState(players=[PlayerState(0,(0,0)) for _ in range(5)], tasks=[TaskState((0,0),0) for _ in range(15)], game_map=np.ndarray((config.map_height,config.map_width)))
    update_sus(action=action,state=state)
    assert state.players[0].sus == action["0"].sus
    assert state.players[1].sus == action["1"].sus
    assert state.players[2].sus == action["2"].sus
    assert state.players[3].sus == action["3"].sus
    assert state.players[4].sus == action["4"].sus
    