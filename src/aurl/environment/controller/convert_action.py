from ..model import PlayerAction
from typing import Dict
from .. import config
import math


def convert_action(action) -> Dict[str, PlayerAction]:
    """convert_action

    step関数に入力されたactionはそのままだと扱いづらいので、こちらで定義したクラスのインスタンスに変換する

    Args:
        action (Any): stepに入力されたaction 型定義不可？

    Returns:
        Dict[str,PlayerAction]: 変換後のアクション情報、キーはプレイヤー番号
    """
    out = {}
    params_per_player = 3 + config.num_players - 1
    for i in range(config.num_players):
        move_raw = action[i * params_per_player + 0]
        move = math.floor(move_raw * 5) if move_raw != 1.0 else 4
        report_raw = action[i * params_per_player + 1]
        report = report_raw > config.act_threshould
        kill_raw = action[i * params_per_player + 2]
        kill = kill_raw > config.act_threshould
        sus_raw = action[
            i * params_per_player
            + 3 : i * params_per_player
            + 3
            + config.num_players
            - 1
        ]
        sus = {}
        for j, s in enumerate(sus_raw):
            sus[str(j)] = s
        player_action = PlayerAction(move=move, report=report, kill=kill, sus=sus)
        out[str(i)] = player_action
    return out
