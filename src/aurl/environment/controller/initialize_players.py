from ..model import PlayerState
from typing import List
from .. import config
import numpy as np


def initialize_players(game_map: np.ndarray) -> List[PlayerState]:
    players = {}
    roles = [0 for _ in range(config.num_players)]
    for imp_idx in np.argsort(np.random.rand(5))[:config.num_imposter]:
        roles[imp_idx] = 1
    mask = game_map == 3
    assert np.count_nonzero(mask) == config.num_players
    spawn_positions = np.where(mask)
    for i in range(config.num_players):
        position = (spawn_positions[0][i], spawn_positions[1][i])
        player_state = PlayerState(role=roles[i], position=position, self_idx=i)
        players[str(i)] = player_state
    return [v for v in players.values()]
