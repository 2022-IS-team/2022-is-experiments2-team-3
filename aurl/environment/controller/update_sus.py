from ..model import GameState, PlayerAction
from typing import Dict


def update_sus(action: Dict[str, PlayerAction], state: GameState) -> None:
    """update_sus

    actionで指定されたsusの値をstate.playersに反映する
    actionの各要素に対して、次を実行する
    1. キーに該当するプレイヤーをstateから参照する
    2. 値を該当プレイヤー要素のsusに代入する

    Args:
        action (Dict[str,PlayerAction]): 各ユーザーの行動
        state (GameState): 現在のゲーム情報
    """
    pass
