from ..model import PlayerAction
from gym.spaces import Space
from typing import Dict


def convert_action(action: Space) -> Dict[str, PlayerAction]:
    """convert_action

    step関数に入力されたactionはそのままだと扱いづらいので、こちらで定義したクラスのインスタンスに変換する

    Args:
        action (Space): stepに入力されたaction

    Returns:
        Dict[str,PlayerAction]: 変換後のアクション情報、キーはプレイヤー番号
    """
    pass
