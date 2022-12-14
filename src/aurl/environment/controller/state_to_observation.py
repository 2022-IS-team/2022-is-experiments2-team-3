from ..model import GameState
from .. import config
import numpy as np
from typing import Dict


def state_to_observation(state: GameState) -> np.ndarray:
    """state_to_observation

    GameStateをobservation_spaceの表現に変換する。

    Args:
        state (GameState): 現状のゲーム情報

    Returns:
        spaces.Space: ゲーム情報を観測に変換したもの
    """
    observation = []
    for i, p in enumerate(state.players):
        player_obs = []
        player_obs += [1.0 if p.dead else 0.0]
        player_obs += [
            p.position[0] / config.map_height,
            p.position[1] / config.map_width,
        ]
        game_map = state.game_map
        game_map = np.where(game_map == 3, 0, game_map)
        player_obs += [
            game_map[p.position[0]][p.position[1]] / 3,
            (game_map[p.position[0] - 1][p.position[1]] if p.position[0] > 0 else 1)
            / 3,
            (
                game_map[p.position[0]][p.position[1] + 1]
                if p.position[1] < config.map_width - 1
                else 1
            )
            / 3,
            (
                game_map[p.position[0] + 1][p.position[1]]
                if p.position[0] < config.map_height - 1
                else 1
            )
            / 3,
            (game_map[p.position[0]][p.position[1] - 1] if p.position[1] > 0 else 1)
            / 3,
        ]
        player_obs += [1.0 if p.failed_to_move else 0.0]
        if p.role == 0:
            player_obs += [
                t.progress / config.num_task_progress_step
                for t in filter(lambda t: t.assignee == i, state.tasks)
            ]
        else:
            player_obs += [1 for _ in range(config.num_tasks_per_player)]
        others_pos = []
        for j, q in enumerate(state.players):
            if i == j:
                continue
            pos = -1
            # 自分が生存時、死亡済みプレイヤーは死体しか見えない
            if q.dead and not p.dead:
                # 死体発見済みなら消失
                if q.reported:
                    pos = 5
                # 未発見なら死体の位置に存在
                elif q.died_at == p.position:
                    pos = 0
                elif q.died_at == (p.position[0] - 1, p.position[1]):
                    pos = 1
                elif q.died_at == (p.position[0], p.position[1] + 1):
                    pos = 2
                elif q.died_at == (p.position[0] + 1, p.position[1]):
                    pos = 3
                elif q.died_at == (p.position[0], p.position[1] - 1):
                    pos = 4
                else:
                    pos = 5
            # 生存他プレイヤー、または自分死亡時に見える他死亡プレイヤー
            elif q.position == p.position:
                pos = 0
            elif q.position == (p.position[0] - 1, p.position[1]):
                pos = 1
            elif q.position == (p.position[0], p.position[1] + 1):
                pos = 2
            elif q.position == (p.position[0] + 1, p.position[1]):
                pos = 3
            elif q.position == (p.position[0], p.position[1] - 1):
                pos = 4
            else:
                pos = 5
            others_pos.append(pos / 6)
        player_obs += others_pos
        others_dead = [(int(k), v) for k, v in p.others_dead.items()]
        others_dead.sort(key=lambda v: v[0])
        player_obs += [1 if v else 0 for _, v in others_dead]
        others_sus = []
        for _, v in [(int(k), v) for k, v in p.others_sus.items()]:
            sus = [(int(k), w) for k, w in v.items()]
            sus.sort(key=lambda w: w[0])
            others_sus += [w for _, w in sus]
        player_obs += others_sus
        player_obs += [p.cooltime / config.kill_cooltime]
        player_obs += [1.0 if p.report_available else 0.0]
        observation += player_obs
    return np.array(observation, dtype=np.float32)
