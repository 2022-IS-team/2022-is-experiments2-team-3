from ..model import GameState
from .. import config


def update_task_progress(state: GameState) -> None:
    """update_task_progress

    全プレイヤーについて、
    タスクリストの中で自分が担当（TaskState.assignee）となっているタスクのうち、
    進捗（TaskState.progress）がconfig.num_task_progress_step未満のものについて、
    - 座標（TaskState.position）が自分の座標（PlayerState.position）と一致していれば、
      進捗に1を加算する
    - 一致していなければ、進捗を0にする

    Args:
        state (GameState): 現在のゲーム情報
    """
