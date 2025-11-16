# Copyright (c) 2025 Matty Chalk
# Licensed under the MIT License (see LICENSE file for details)

"""Testing module for maze_runner.py."""

from maze import *
from maze_runner import *


def test_shortest_path():
    """Unit test shortest_path."""
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


def test_maze_reader():
    """Unit test maze_reader."""
    tiny_maze = maze_reader("src/tiny_maze.mz")
    assert get_dimensions(tiny_maze) == (1, 1)
    assert get_walls(tiny_maze, 0, 0) == (True, True, True, True)

    medium_empty_maze = maze_reader("src/medium_empty_maze.mz")
    assert get_dimensions(medium_empty_maze) == (3, 3)
    assert get_walls(medium_empty_maze, 0, 0) == (False, False, True, True)
    assert get_walls(medium_empty_maze, 2, 0) == (False, True, True, False)
    assert get_walls(medium_empty_maze, 2, 2) == (True, True, False, False)
    assert get_walls(medium_empty_maze, 0, 2) == (True, False, False, True)
    assert get_walls(medium_empty_maze, 1, 1) == (False, False, False, False)

    medium_maze = maze_reader("src/medium_maze.mz")
    assert get_dimensions(medium_maze) == (3, 3)

    # Maze looks like this:
    # # # # # # #
    # . . . # . #
    # . # # # . #
    # . . . . . #
    # . # # # . #
    # . # . . . #
    # # # # # # #

    assert get_walls(medium_maze, 0, 0) == (False, True, True, True)
    assert get_walls(medium_maze, 1, 0) == (True, False, True, True)
    assert get_walls(medium_maze, 2, 0) == (False, True, True, False)

    assert get_walls(medium_maze, 0, 1) == (False, False, False, True)
    assert get_walls(medium_maze, 1, 1) == (True, False, True, False)
    assert get_walls(medium_maze, 2, 1) == (False, True, False, False)

    assert get_walls(medium_maze, 0, 2) == (True, False, False, True)
    assert get_walls(medium_maze, 1, 2) == (True, True, True, False)
    assert get_walls(medium_maze, 2, 2) == (True, True, False, True)
