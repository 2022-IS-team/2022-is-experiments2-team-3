from ..model import GameState
from .. import config


def judge(state: GameState) -> str:
    """judge

    ゲーム情報から勝敗を判定する
    1. インポスターが全員死亡していればクルーの勝ち
    2. タスクが全て完了していればクルーの勝ち
    3. クルーの生存数がインポスターの生存数以下であったらインポスターの勝ち
    4. 上記のどれも当てはまらなければゲーム続行

    Args:
        state (GameState): 現在のゲーム情報

    Returns:
        str: 勝敗判定の結果 "crew"=クルーの勝ち "imposter"=インポスターの勝ち "continue"=ゲーム続行
    """
    num_crew = 0
    num_imposter = 0
    for p in state.players:
        if p.dead:
            continue
        if p.role == 0:
            num_crew += 1
        else:
            num_imposter += 1
    if num_imposter == 0:
        return "crew"
    if num_crew <= num_imposter:
        return "imposter"

    is_task_completed = True
    for t in state.tasks:
        if t.progress < config.num_task_progress_step:
            is_task_completed = False
            break
    if is_task_completed:
        return "crew"
    return "continue"