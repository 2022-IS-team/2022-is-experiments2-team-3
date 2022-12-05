from gym import spaces
from .. import config
import numpy as np
import copy
import functools


def define_spaces():
    """
    observation_space, action_spaceを定義
    """
    player_obs_space = spaces.Dict(
        spaces={
            "dead": spaces.Discrete(2),
            "position": spaces.Box(
                low=np.array([0.0, 0.0]),
                high=np.array([config.map_height, config.map_width]),
                dtype=np.uint8,
            ),
            # 0=移動可能 1=移動不可 2=タスク
            "surroundings": spaces.Dict(
                {
                    "here": spaces.Discrete(3),
                    "up": spaces.Discrete(3),
                    "right": spaces.Discrete(3),
                    "down": spaces.Discrete(3),
                    "left": spaces.Discrete(3),
                }
            ),
            "failed_to_move": spaces.Discrete(2),
            "tasks": spaces.Box(
                low=0.0,
                high=1.0,
                shape=(config.num_tasks_per_player,),
                dtype=np.float32,
            ),
            # 0=同じマス 1~4=上右下左 5=不明
            "others_pos": spaces.MultiDiscrete(
                [6 for _ in range(config.num_players - 1)]
            ),
            "others_dead": spaces.MultiDiscrete(
                [2 for _ in range(config.num_players - 1)]
            ),
            "others_sus": spaces.Box(
                low=0.0,
                high=1.0,
                shape=(config.num_players - 1, config.num_players - 1),
                dtype=np.float32,
            ),
            "cooltime": spaces.Box(low=0.0, high=1.0, shape=(), dtype=np.float32),
            "report_available": spaces.Discrete(2),
        }
    )

    def dup_player_obs(acc, i):
        acc[str(i)] = copy.deepcopy(player_obs_space)
        return acc

    observation_space = spaces.Dict(
        functools.reduce(dup_player_obs, range(config.num_players), {})
    )

    """
    [移動,報告,キル,sus値x(pl数-1)]xpl数 となる
    移動は
      0.0<=x<0.2: 停止
      0.2<=x<0.4: 上
      0.4<=x<0.6: 右
      0.6<=x<0.8: 下
      0.8<=x<=1.0: 左
    報告・キルは、act_threthouldを超えたら実行判定
    """
    action_space = spaces.Box(
        low=0.0,
        high=1.0,
        shape=((2 + config.num_players - 1) * config.num_players,),
        dtype=np.float32,
    )

    return observation_space, action_space
