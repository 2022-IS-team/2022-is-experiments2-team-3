from ..model import GameState
from .. import config
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
        reward = -1
        for task in state.tasks:
            if task.assignee == i:
                continue
            if task.progress == 0 or task.progress == config.num_task_progress_step:
                continue
            reward += 1
            break
        rewards[str(i)] = reward
    return rewards
