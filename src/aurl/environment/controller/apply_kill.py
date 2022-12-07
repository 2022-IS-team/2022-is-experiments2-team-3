from ..model import GameState, PlayerAction
from typing import Dict
from .. import config


def apply_kill(action: Dict[str, PlayerAction], state: GameState) -> None:
    """apply_kill

    全プレイヤーのアクションのうち、
    - キルを実行している
    もののなかで、そのアクションを実行するプレイヤーで、
    - インポスターである
    - 生存している
    - キル可能である（PlayerState.cooltime == 0）
    - 現在いるマスと同じマスに、
        - クルーである
        - 生存している
        を満たすプレイヤーが存在する。
    を満たすものがいれば、
    - 同じ座標にいる生存クルーを死亡判定とする。
    - 自分のクールタイムをconfig.kill_cooltimeに設定する。

    Args:
        action (Dict[str,PlayerAction]): 全プレイヤーの行動
        state (GameState): 現在のゲーム情報
    """

    for i, a in action.items():
        if not a.kill:
            continue
        player_state = state.players[int(i)]
        if not player_state.role == 1 or player_state.dead or player_state.cooltime > 0:
            continue
        for j, p in enumerate(state.players):
            if i == j:
                continue
            if p.role != 0:
                continue
            if p.dead:
                continue
            if p.position != player_state.position:
                continue
            p.dead = True
            p.died_at = p.position
            player_state.cooltime = config.kill_cooltime
            break
