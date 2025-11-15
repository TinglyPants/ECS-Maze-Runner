# Copyright (c) 2025 Matty Chalk
# Licensed under the MIT License (see LICENSE file for details)

"""Testing module for maze_runner.py."""

from maze import *
from maze_runner import *


def test_shortest_path():
    """Unit test shortest path."""
    maze = create_maze(11, 5)
    maze = add_horizontal_wall(maze, 0, 1)
    maze = add_vertical_wall(maze, 1, 1)
    path = shortest_path(maze)
    assert path[0] == (0, 0, "RF")
    assert path[-1] == (9, 4, "F")
    prefix = []
    for location in path:
        x, y, a = location
        assert (x, y) not in prefix, f"{location} is repeated"
        prefix.append((x, y))
