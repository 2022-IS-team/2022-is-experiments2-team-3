from ..model import GameState
from .. import config
import numpy as np
from typing import Dict


def state_to_observation(state: GameState) -> Dict[str, Dict]:
    """state_to_observation

    GameStateをobservation_spaceの表現に変換する。

    Args:
        state (GameState): 現状のゲーム情報

    Returns:
        spaces.Space: ゲーム情報を観測に変換したもの
    """
    observation = {}
    for i, p in enumerate(state.players):
        player_obs = {}
        player_obs["dead"] = 1 if p.dead else 0
        player_obs["position"] = np.array([p.position[0], p.position[1]])
        game_map = state.game_map
        game_map = np.where(game_map == 3, 0, game_map)
        player_obs["surroundings"] = {
            "here": game_map[p.position[0]][p.position[1]],
            "up": game_map[p.position[0] - 1][p.position[1]]
            if p.position[0] > 0
            else 1,
            "right": game_map[p.position[0]][p.position[1] + 1]
            if p.position[1] < config.map_width - 1
            else 1,
            "down": game_map[p.position[0] + 1][p.position[1]]
            if p.position[0] < config.map_height - 1
            else 1,
            "left": game_map[p.position[0]][p.position[1] - 1]
            if p.position[1] > 0
            else 1,
        }
        player_obs["failed_to_move"] = 1 if p.failed_to_move else 0
        player_obs["tasks"] = np.array(
            [
                t.progress / config.num_task_progress_step
                for t in filter(lambda t: t.assignee == i, state.tasks)
            ]
        )
        player_obs["others_pos"] = []
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
            player_obs["others_pos"].append(pos)
        others_dead = [(int(k), v) for k, v in p.others_dead.items()]
        others_dead.sort(key=lambda v: v[0])
        player_obs["others_dead"] = [1 if v else 0 for _, v in others_dead]
        others_sus = []
        for _, v in [(int(k), v) for k, v in p.others_sus.items()]:
            sus = [(int(k), w) for k, w in v.items()]
            sus.sort(key=lambda w: w[0])
            others_sus.append([w for _, w in sus])
        player_obs["others_sus"] = np.array(others_sus)
        player_obs["cooltime"] = np.array([p.cooltime / config.kill_cooltime])
        player_obs["report_available"] = 1 if p.report_available else 0
        observation[str(i)] = player_obs
    return observation
