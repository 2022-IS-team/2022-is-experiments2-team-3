from ..model import GameState
from gym import spaces


def state_to_observation(state: GameState) -> spaces.Space:
    """state_to_observation

    GameStateをobservation_spaceの表現に変換する。

    Args:
        state (GameState): 現状のゲーム情報

    Returns:
        spaces.Space: ゲーム情報を観測に変換したもの
    """
    pass
