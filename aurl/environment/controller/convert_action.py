from ..model import PlayerAction
from typing import Dict


def convert_action(action) -> Dict[str, PlayerAction]:
    """convert_action

    step関数に入力されたactionはそのままだと扱いづらいので、こちらで定義したクラスのインスタンスに変換する

    Args:
        action (Any): stepに入力されたaction 型定義不可？

    Returns:
        Dict[str,PlayerAction]: 変換後のアクション情報、キーはプレイヤー番号
    """
    out = {}
    for i, a in action.items():
        sus = {}
        for j, sus_value in enumerate(a[3]):
            sus[str(j if j < int(i) else j + 1)] = sus_value
        player_action = PlayerAction(a[0], a[1] == 1, a[2] == 1, sus)
        out[i] = player_action
    return out
