from ..model import GameState, PlayerAction
from typing import Dict


def someone_reported(action: Dict[str, PlayerAction], state: GameState) -> bool:
    """someone_reported

    一人以上のプレイヤーに対し、以下がすべて成り立つとき、Trueを返す
    - クルーである（該当するPlayerState.role == 0）
    - 通報をしている（PlayerAction.reportがTrue)
    - 通報可能である（該当するPlayerState.report_availableがTrue）

    Args:
        action (Dict[str,PlayerAction]): 全プレイヤーのアクション
        state (GameState): 現在のゲーム情報

    Returns:
        bool: 通報が有効であればTrue
    """
    pass
