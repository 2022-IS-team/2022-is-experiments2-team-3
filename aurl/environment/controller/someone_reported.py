from ..model import GameState, PlayerAction
from typing import Dict


def someone_reported(action: Dict[str, PlayerAction], state: GameState) -> bool:
    """someone_reported

    一人以上のプレイヤーに対し、
    - クルーである（該当するPlayerState.role == 0）
    - 通報をしている（PlayerAction.reportがTrue)
    - 通報可能である（該当するPlayerState.report_availableがTrue）
    がすべて成り立つとき、
    全てのプレイヤーの中で、
    - クルーである
    - 現在死亡している
    - 死体が発見されている(PlayerState.reportedがFalse)
    が成り立つプレイヤーを発見済み(PlayerState.reported=True)として、
    関数の返り値としてTrueを返す。

    最初の条件に該当するプレイヤーがいない場合はFalseを返す。

    Args:
        action (Dict[str,PlayerAction]): 全プレイヤーのアクション
        state (GameState): 現在のゲーム情報

    Returns:
        bool: 通報が有効であればTrue
    """
    pass
