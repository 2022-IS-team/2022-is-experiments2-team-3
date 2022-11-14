from ..model import GameState
from typing import Dict


def calc_reward_on_reported(state: GameState, reported_by: int) -> Dict[str, float]:
    """calc_reward_on_reported

    死体発見時の報酬を計算する

    Args:
        state (GameState): 現在のゲーム情報

    Returns:
        Dict[str, float]: 報酬
    """
    rewards = {}
    for i, p in enumerate(state.players):
        if i == reported_by and p.role == 0:
            rewards[str(i)] = 10
        else:
            rewards[str(i)] = 0
    return rewards
