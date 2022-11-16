from ..model import GameState


def reset_failed_to_move(state: GameState) -> None:
    """reset_failed_to_move

    各プレイヤーの壁衝突判定をリセットする
    state.playersの全ての要素に対して、以下を実行する
    1. failed_to_moveをFalseにする

    Args:
        state (GameState): 現在のゲーム情報
    """
    for i in state.players:
        i.failed_to_move = False
