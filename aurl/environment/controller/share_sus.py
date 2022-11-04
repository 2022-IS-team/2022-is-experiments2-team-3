from ..model import GameState


def share_sus(state: GameState) -> None:
    """share_sus

    プレイヤー同士が互いにsusの値を共有する。
    state.playersの各値について次を行う。
    1. state.playersの当該要素以外の要素(:ref:PlayerState)のsusのリストを、当該要素のothers_susに代入する

    Args:
        state (GameState): 現在のゲーム情報
    """
    pass
