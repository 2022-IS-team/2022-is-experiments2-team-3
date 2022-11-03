num_players = 5


class PlayerState:
    def __init__(self, role, position):
        self.role = role
        self.dead = False
        self.position = position
        self.sus = [0 for _ in range(num_players - 1)]
        self.others_sus = [
            [0 for _ in range(num_players - 1)] for _ in range(num_players - 1)
        ]
        self.failed_to_move = False
        self.cooltimes = [0, 0, 0, 0]


class TaskState:
    def __init__(self, position):
        self.position = position
        self.progress = 0


class GameState:
    def __init__(self, players, tasks, game_map):
        self.players = [PlayerState(role, position) for role, position in players]
        self.tasks = [TaskState(position) for position in tasks]
        self.game_map = game_map
        self.meeting = False
