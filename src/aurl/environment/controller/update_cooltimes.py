from ..model import GameState


def update_cooltimes(state: GameState) -> None:
    """update_cooltimes

    全プレイヤーのうち、
    - インポスターである
    - クールタイム（PlayerState.cooltime）が1以上である
    ものについて、クールタイムを1減らす

    Args:
        state (GameState): 現在のゲーム情報
    """
