from ..model import GameState


def update_report_availability(state: GameState) -> None:
    """update_report_availability

    各プレイヤーのうち生存しているものがいるマスに死体が存在すれば、そのプレイヤーを通報可能とする。
    死体は、全プレイヤーの中で、
    - クルーである
    - 死亡している
    - 死体が発見されていない(PlayerState.reported==False)
    - 死亡座標(PlayerState.died_at)が、発見するプレイヤーの座標と一致する
    を満たすとき存在する。

    Args:
        state (GameState): 現在のゲーム情報
    """
    for i, p in enumerate(state.players):
        p.report_available = False
        for j, q in enumerate(state.players):
            if i != j:
                if q.role == 0:
                    if q.dead == True:
                        if q.reported == False:
                            if p.position == q.died_at:
                               p.report_available = True
                               break

