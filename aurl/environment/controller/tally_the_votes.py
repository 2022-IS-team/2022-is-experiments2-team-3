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
    votes = [0 for _ in range(config.num_players + 1)]
    for i, p in enumerate(state.players):
        max_sus = -1
        max_key = None
        for k, v in p.sus.items():
            if v >= config.vote_threshould and v > max_sus:
                max_sus = v
                max_key = k
        if max_key is None:
            votes[config.num_players] += 1
        else:
            votes[int(max_key)] += 1

    max_votes = 0
    max_idx = None
    for i, v in enumerate(votes):
        if v == max_votes:
            max_idx = None
        elif v > max_votes:
            max_votes = v
            max_idx = i

    if max_idx is None:
        return
    if max_idx == config.num_players:
        return

    state.players[max_idx].dead = True
