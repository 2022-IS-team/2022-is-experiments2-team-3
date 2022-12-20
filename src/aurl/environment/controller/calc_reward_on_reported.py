from ..model import GameState
from typing import Dict


def calc_reward_on_reported(state: GameState) -> Dict[str, float]:
    """calc_reward_on_reported

    死体発見時の報酬を計算する

    Args:
        state (GameState): 現在のゲーム情報

    Returns:
        Dict[str, float]: 報酬
    """
    rewards = {}
    for i, p in enumerate(state.players):
        if p.role == 0:
            rewards[str(i)] = -5
        elif p.role == 1:
            rewards[str(i)] = -1
    return rewards
