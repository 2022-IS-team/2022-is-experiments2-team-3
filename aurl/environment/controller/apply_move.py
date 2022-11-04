from ..model import GameState, PlayerAction
from typing import Dict


def apply_move(action: Dict[str, PlayerAction], state: GameState) -> None:
    """apply_move

    すべてのプレイヤーの行動のうち、
    - 移動方向(PlayerAction.move)が0=静止以外
    を満たすものに対し、
    該当するプレイヤーの座標(PlayerState.position)を移動方向に1移動させた先が、
    マップ(state.game_map)上の移動不可マス(値が1)であれば、移動失敗とする（PlayerState.failed_to_move=True)
    そうでなければ座標を移動先の座標へ書き換える。

    Args:
        action (Dict[str,PlayerAction]): 全プレイヤーの行動
        state (GameState): 現在のゲーム情報
    """
    pass
