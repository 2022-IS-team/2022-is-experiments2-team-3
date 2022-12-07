from ..model import GameState


def share_dead(state: GameState) -> None:
    for i, p in enumerate(state.players):
        for j, q in enumerate(state.players):
            if i == j:
                continue
            p.others_dead[str(j)] = q.dead
