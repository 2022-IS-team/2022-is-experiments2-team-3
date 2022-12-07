from ..model import GameState
from typing import Dict


def calc_reward_on_working(state: GameState) -> Dict[str, float]:
    """calc_reward_on_working

    行動フェーズの報酬を計算する

    Args:
        state (GameState): 現在のゲーム情報

    Returns:
        Dict[str, float]: 報酬
    """
    rewards = {}
    for i, p in enumerate(state.players):
        reward = 0
        if p.failed_to_move:
            reward -= 1
        rewards[str(i)] = reward
    return rewards
