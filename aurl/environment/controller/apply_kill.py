from ..model import GameState, PlayerAction
from typing import Dict


def apply_kill(action: Dict[str, PlayerAction], state: GameState) -> None:
    """apply_kill

    全プレイヤーのアクションのうち、
    - キルを実行している
    もののなかで、そのアクションを実行するプレイヤーで、
    - インポスターである
    - 生存している
    - キル可能である（PlayerState.cooltime == 0）
    - 現在いるマスと同じマスに、
        - クルーである
        - 生存している
        を満たすプレイヤーが存在する。
    を満たすものがいれば、
    - 同じ座標にいる生存クルーを死亡判定とする。
    - 自分のクールタイムをconfig.kill_cooltimeに設定する。

    Args:
        action (Dict[str,PlayerAction]): 全プレイヤーの行動
        state (GameState): 現在のゲーム情報
    """
    pass
