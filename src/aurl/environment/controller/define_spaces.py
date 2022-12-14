from gym import spaces
from .. import config
import numpy as np


def define_spaces():
    """
    observation_space, action_spaceを定義
    """
    # [
    #   dead, <- 0 or 1
    #   position[2], <- (x,y)
    #   surroundings-here,surroundings-up,surroundings-right,surroundings-down,surroundings-left,
    #   <- 0(移動可能) | 1/3(移動不可) | 2/3(タスク)
    #   failed_to_move, <- 0 or 1
    #   tasks[num_tasks], <- 連続値
    #   others_pos[num_pl-1], <- 0(here) | 1/6(up) | 2/6(right) | 3/6(down) | 4/6(left) | 5/6(unknown)
    #   others_dead[num_pl-1], <- 0 or 1
    #   others_sus[num_pl-1][num_pl-1], <- 連続値
    #   cooltime, <- 連続値
    #   report_available, <- 0 or 1
    # ] x num_pl
    observation_space = spaces.Box(
        low=0.0,
        high=1.0,
        shape=(
            (
                11
                + config.num_tasks_per_player
                + (config.num_players - 1) * 2
                + (config.num_players - 1) * (config.num_players - 1)
            )
            * config.num_players,
        ),
        dtype=np.float32,
    )

    # [move,report,kill,sus[pl数-1]]xpl数 となる
    # moveは
    #   0.0<=x<0.2: 停止
    #   0.2<=x<0.4: 上
    #   0.4<=x<0.6: 右
    #   0.6<=x<0.8: 下
    #   0.8<=x<=1.0: 左
    # report・killは、act_threthouldを超えたら実行判定
    action_space = spaces.Box(
        low=0.0,
        high=1.0,
        shape=((3 + config.num_players - 1) * config.num_players,),
        dtype=np.float32,
    )

    return observation_space, action_space
