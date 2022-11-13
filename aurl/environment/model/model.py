from .. import config
from typing import Tuple, List, Dict
import numpy as np


class PlayerState:
    """PlayerState

    プレイヤー情報を格納するクラス

    """

    role: int
    dead: bool
    position: Tuple[int, int]
    sus: Dict[str, float]
    others_dead: List[bool]
    others_sus: Dict[str, Dict[str, float]]
    failed_to_move: bool
    report_available: bool
    cooltime: int
    died_at: Tuple[int, int] or None
    reported: bool

    def __init__(self, role: int, position: Tuple[int, int], self_idx: int):
        """__init__

        Args:
            role (int): プレイヤーの役 0=crew 1=imposter
            position (Tuple[int, int]): 初期座標
            self_idx (int): 自プレイヤーのインデックス
        """
        assert role == 0 or role == 1
        self.role = role
        self.dead = False
        self.position = position
        self.sus = [0.0 for _ in range(config.num_players - 1)]
        self.others_dead = [False for _ in range(config.num_players - 1)]
        self.others_sus = {}
        for i in range(config.num_players):
            if i == self_idx:
                continue
            sus = {}
            for j in range(config.num_players):
                if i == j:
                    continue
                sus[str(j)] = 0.0
            self.others_sus[str(i)] = sus
        self.failed_to_move = False
        self.report_available = False
        self.cooltime = 0
        self.died_at = None
        self.reported = False


class TaskState:
    """TaskState

    タスクの情報を格納するクラス

    """

    position: Tuple[int, int]
    assignee: int
    progress: int

    def __init__(self, position: Tuple[int, int], assignee: int):
        """__init__

        Args:
            position (Tuple[int, int]): 配置する座標
            assignee (int): 担当するプレイヤー番号
        """
        self.position = position
        assert assignee < config.num_players
        self.assignee = assignee
        self.progress = 0


class GameState:
    """GameState

    すべてのゲーム情報を格納するクラス

    """

    players: List[PlayerState]
    tasks: List[TaskState]
    game_map: np.ndarray
    meeting: bool
    # sabotages: List[bool]

    def __init__(
        self, players: List[PlayerState], tasks: List[TaskState], game_map: np.ndarray
    ):
        """__init__

        Args:
            players (List[PlayerState]): プレイヤー情報のリスト
            tasks (List[TaskState]): タスク情報のリスト
            game_map (np.ndarray): マップ情報
        """
        self.players = players
        self.tasks = tasks
        assert game_map.shape == (config.map_height, config.map_width)
        self.game_map = game_map
        self.meeting = False
        # self.sabotages = [False, False, False]


class PlayerAction:
    """PlayerAction"""

    move: int
    report: bool
    kill: bool
    sus: List[float]

    def __init__(self, move: int, report: bool, kill: bool, sus: Dict[str, float]):
        """__init__

        Args:
            move (int): 移動方向 0=静止 1=上 2=右 3=下 4=左
            report (bool): 通報するか（クルーのみ有効）
            kill (bool): 殺害するか（インポスターのみ有効）
            sus (Dict[str,float]): 他プレイヤーをどれくらい疑っているか
        """
        self.move = move
        self.report = report
        self.kill = kill
        self.sus = sus
