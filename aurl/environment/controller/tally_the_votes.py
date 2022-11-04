from ..model import GameState
from .. import config


def tally_the_votes(state: GameState) -> None:
    """tally_the_votes

    1. 全プレイヤーのsus値から投票を判定する
        - sus値がconfig.vote_threshouldを超えている対象がいなければ、無投票とみなす
        - sus値がconfig.vote_threshouldを超えている対象がいる場合、sus値が最大の対象に投票したとみなす
        - 一人一票である
    2. 一番多い意見を採用する
        - 無投票が多ければ何もせず終了する
        - 票数が同着1位であった場合、何もせず終了する
    3. 追放対象のプレイヤーを死亡判定とする
        - PlayerState.deadをTrueにする

    Args:
        state (GameState): 現在のゲーム情報
    """
    pass
