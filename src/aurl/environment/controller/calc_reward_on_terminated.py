from ..model import GameState
from typing import Dict


def calc_reward_on_terminated(state: GameState, judge: str) -> Dict[str, float]:
    """calc_reward_on_terminated

    ゲーム終了時の報酬を計算する。

    Args:
        state (GameState): 現状のゲーム情報
        judge (str): 勝敗判定　"crew"=クルー陣営の勝利 "imposter"=インポスター陣営の勝利

    Returns:
        Dict[str, float]: 報酬
    """
    rewards = {}
    for i, p in enumerate(state.players):
        if p.role == 0:
            if judge == "crew":
                rewards[str(i)] = 100
            elif judge == "imposter":
                rewards[str(i)] = -100
        elif p.role == 1:
            if judge == "crew":
                rewards[str(i)] = -100
            elif judge == "imposter":
                rewards[str(i)] = 100
    return rewards
