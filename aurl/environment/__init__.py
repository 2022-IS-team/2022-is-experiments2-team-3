from . import controller, model
from .environment import AUEnv
from gym.envs.registration import register

__all__ = ["AUEnv", "controller", "model"]

register(id="isteam3/MockAmongUs-v0", entry_point="aurl.environment:AUEnv")
