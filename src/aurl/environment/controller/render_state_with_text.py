from ..model import GameState
from .. import config
import numpy as np
from typing import Dict
from io import StringIO
from contextlib import closing
from itertools import zip_longest


def render_state_with_text(state: GameState) -> str:
    outfile = StringIO()
    map_lines = []
    info_lines = []

    map_lines.append("┌" + "-" * (config.map_width * 2) + "┐")
    for y in range(config.map_height):
        line = "|"
        for x in range(config.map_width):
            map_cell = state.game_map[y][x]
            if map_cell == 0:
                output = [" ", " "]
            elif map_cell == 1:
                output = ["X", "X"]
            elif map_cell == 2:
                output = ["T", " "]
            elif map_cell == 3:
                output = [" ", " "]
            else:
                output = [" ", " "]
            for i, p in enumerate(state.players):
                if p.position == (y, x):
                    if output[1] == " ":
                        output[1] = str(i)
                    else:
                        output[1] = "C"
            line += "".join(output)
        line += "|"
        map_lines.append(line)
    map_lines.append("└" + "-" * (config.map_width * 2) + "┘")

    info_lines.append("<Players>")
    for i, p in enumerate(state.players):
        sus_str = "["
        for j in range(config.num_players):
            if i == j:
                sus_str += "___"
            else:
                sus_str += "%.1f" % p.sus[str(j)]
            sus_str += ","
        sus_str = sus_str.rstrip()
        sus_str += "]"
        info_lines.append(
            "P%d:%1s%1s (%d,%d) %s"
            % (
                i,
                "C" if p.role == 0 else "I",
                "D" if p.dead else "",
                p.position[0],
                p.position[1],
                sus_str,
            )
        )
    info_lines.append("")
    info_lines.append("<Tasks>")
    tasks_head = ""
    tasks_progresses = ""
    key = 0
    for i in range(config.num_players):
        if state.players[i].role == 1:
            continue
        for j in range(config.num_tasks_per_player):
            tasks_head += "T%1d%1d " % (i, j)
            tasks_progresses += "%3d " % (state.tasks[key].progress)
            key += 1
        tasks_head = tasks_head.rstrip()
        tasks_progresses = tasks_progresses.rstrip()
        tasks_head += "|"
        tasks_progresses += "|"
    tasks_head = tasks_head.rstrip("|")
    tasks_progresses = tasks_progresses.rstrip("|")
    tasks_progresses += " / %d" % (config.num_task_progress_step)
    info_lines.append(tasks_head)
    info_lines.append(tasks_progresses)

    for map_line, info_line in zip_longest(map_lines, info_lines):
        if not map_line is None:
            outfile.write(map_line)
        else:
            outfile.write(" " * (config.map_width * 2 + 2))
        outfile.write(" ")
        if not info_line is None:
            outfile.write(info_line)
        outfile.write("\n")

    with closing(outfile):
        return outfile.getvalue()
