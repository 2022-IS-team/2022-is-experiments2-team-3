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
