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
    players_num = len(state.players)
    vote = [0] * players_num
    for i in range(players_num):
      sus_val = state.players[i].sus.values()
      max_sus = max(sus_val)
      max_ind = sus_val.index(max_sus)
      if max(sus_val) > config.vote_threshould and i >= max_ind:
        vote[max_ind+1] = vote[max_ind+1]+1
      elif max(sus_val) > config.vote_threshould and i < max_ind:
        vote[max_ind] = vote[max_ind]+1
    max_vote = max(vote)
    sum_vote = sum(vote)
    count_max = vote.count(max_vote)
    max_index = vote.index(max_vote)
    if sum_vote < players_num / 2:
      pass
    elif count_max > 1:
      pass
    else:
      state.players[max_index].dead = True
