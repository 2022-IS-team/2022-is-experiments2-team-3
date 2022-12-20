from ..model import GameState
from typing import Dict


def calc_reward_on_meeting(state: GameState) -> Dict[str, float]:
    """calc_reward_on_meeting

    会議フェーズ時の報酬

    Args:
        state (GameState): 現状のゲーム情報

    Returns:
        Dict[str, float]: 報酬
    """
    rewards = {}
    for i, p in enumerate(state.players):
        if p.role == 0:
            rewards[str(i)] = -1
        elif p.role == 1:
            imposters = sum(
                [1 if not p.dead and p.role == 1 else 0 for p in state.players]
            )
            rewards[str(i)] = 10 * imposters
    return rewards
