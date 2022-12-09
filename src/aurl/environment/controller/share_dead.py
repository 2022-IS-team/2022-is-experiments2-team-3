from ..model import GameState


def share_dead(state: GameState) -> None:
    """share_sus

    プレイヤー同士が互いにsusの値を共有する。
    state.playersの各値について次を行う。
    1. state.playersの当該要素以外の要素(:ref:PlayerState)が死亡しているかどうかを、当該要素のothers_deadに代入する。これはbooleanの配列

    Args:
        state (GameState): 現在のゲーム情報
    """
    for i, p in enumerate(state.players):
        others_dead = {}
        for j, q in enumerate(state.players):
            if i == j:
                continue
            others_dead[str(j)] = q.dead
            state.players[i].others_dead = others_dead
