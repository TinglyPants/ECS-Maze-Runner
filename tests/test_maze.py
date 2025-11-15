# Copyright (c) 2025 Matty Chalk
# Licensed under the MIT License (see LICENSE file for details)

"""Testing module for maze.py."""

import pytest
from maze import *


def test_create_maze_assignment():
    """Unit test create_maze assignment."""
    default_maze = create_maze()
    assert len(default_maze) == 5
    assert len(default_maze[0]) == 5

    # Corners
    assert default_maze[0][0] == [False, False, True, True]  # BL
    assert default_maze[0][4] == [True, False, False, True]  # TL
    assert default_maze[4][0] == [False, True, True, False]  # BR
    assert default_maze[4][4] == [True, True, False, False]  # TR

    # Middle of maze
    assert default_maze[2][2] == [False, False, False, False]

    # Edges
    assert default_maze[2][4] == [True, False, False, False]  # Top
    assert default_maze[4][2] == [False, True, False, False]  # Right
    assert default_maze[2][0] == [False, False, True, False]  # Bottom
    assert default_maze[0][2] == [False, False, False, True]  # Left

    tiny_maze = create_maze(1, 1)
    assert tiny_maze[0][0] == [True, True, True, True]

    big_maze = create_maze(50, 50)
    assert len(big_maze) == 50
    assert len(big_maze[0]) == 50


def test_create_maze_type_validation():
    """Unit test create_maze type validation."""
    with pytest.raises(TypeError):
        create_maze(width="Not an integer")
    with pytest.raises(TypeError):
        create_maze(height="Not an integer")

    with pytest.raises(ValueError):
        create_maze(height=0)
    with pytest.raises(ValueError):
        create_maze(width=0)
    with pytest.raises(ValueError):
        create_maze(height=-1)
    with pytest.raises(ValueError):
        create_maze(width=-1)


def test_add_horizontal_wall_assignment():
    """Unit test add_horizontal_wall assignment."""
    maze = create_maze()

    maze = add_horizontal_wall(maze, 2, 2)
    assert maze[2][2] == [False, False, True, False]
    assert maze[2][1] == [True, False, False, False]


def test_add_horizontal_wall_type_validation():
    """Unit test add_horizontal_wall type validation."""
    maze = create_maze()
    with pytest.raises(TypeError):
        add_horizontal_wall(maze, "Not an integer", 1)
    with pytest.raises(TypeError):
        add_horizontal_wall(maze, 1, "Not an integer")

    with pytest.raises(ValueError):
        add_horizontal_wall(maze, -1, 1)
    with pytest.raises(ValueError):
        add_horizontal_wall(maze, 5, 1)

    with pytest.raises(ValueError):
        add_horizontal_wall(maze, 0, -1)
    with pytest.raises(ValueError):
        add_horizontal_wall(maze, 0, 0)
    with pytest.raises(ValueError):
        add_horizontal_wall(maze, 0, 5)
    with pytest.raises(ValueError):
        add_horizontal_wall(maze, 0, 6)


def test_add_vertical_wall_assignment():
    """Unit test add_vertical_wall assignment."""
    maze = create_maze()

    maze = add_vertical_wall(maze, 2, 2)
    assert maze[2][2] == [False, False, False, True]
    assert maze[1][2] == [False, True, False, False]


def test_add_vertical_wall_type_validation():
    """Unit test add_vertical_wall type validation."""
    maze = create_maze()
    with pytest.raises(TypeError):
        add_vertical_wall(maze, "Not an integer", 1)
    with pytest.raises(TypeError):
        add_vertical_wall(maze, 1, "Not an integer")

    with pytest.raises(ValueError):
        add_vertical_wall(maze, -1, 1)
    with pytest.raises(ValueError):
        add_vertical_wall(maze, 5, 1)

    with pytest.raises(ValueError):
        add_vertical_wall(maze, 0, -1)
    with pytest.raises(ValueError):
        add_vertical_wall(maze, 0, 0)
    with pytest.raises(ValueError):
        add_vertical_wall(maze, 0, 5)
    with pytest.raises(ValueError):
        add_vertical_wall(maze, 0, 6)


def test_get_dimensions_assignment():
    """Unit test get_dimensions assignment."""
    default_maze = create_maze()
    assert get_dimensions(default_maze) == (5, 5)

    tiny_maze = create_maze(1, 1)
    assert get_dimensions(tiny_maze) == (1, 1)

    big_maze = create_maze(50, 100)
    assert get_dimensions(big_maze) == (50, 100)


def test_get_dimensions_type_validation():
    """Unit test get_dimensions type validation."""
    with pytest.raises(TypeError):
        get_dimensions(1)
    with pytest.raises(TypeError):
        get_dimensions([1, 2, 3])

    with pytest.raises(ValueError):
        get_dimensions([["Jagged"], [1, 2]])


def test_get_walls_assignment():
    """Unit test get_walls assignment."""
    default_maze = create_maze()

    # Corners
    assert get_walls(default_maze, 0, 0) == (False, False, True, True)  # BL
    assert get_walls(default_maze, 0, 4) == (True, False, False, True)  # TL
    assert get_walls(default_maze, 4, 0) == (False, True, True, False)  # BR
    assert get_walls(default_maze, 4, 4) == (True, True, False, False)  # TR

    # Middle of maze
    assert get_walls(default_maze, 2, 2) == (False, False, False, False)

    # Edges
    assert get_walls(default_maze, 2, 4) == (True, False, False, False)  # Top
    assert get_walls(default_maze, 4, 2) == (False, True, False, False)  # Right
    assert get_walls(default_maze, 2, 0) == (False, False, True, False)  # Bottom
    assert get_walls(default_maze, 0, 2) == (False, False, False, True)  # Left


def test_get_walls_type_validation():
    """Unit test get_walls type validation."""
    maze = create_maze()
    with pytest.raises(TypeError):
        get_walls(maze, "Not an integer", 1)
    with pytest.raises(TypeError):
        get_walls(maze, 1, "Not an integer")

    with pytest.raises(ValueError):
        get_walls(maze, -1, 1)
    with pytest.raises(ValueError):
        get_walls(maze, 1, -1)

    with pytest.raises(ValueError):
        get_walls(maze, 5, 1)
    with pytest.raises(ValueError):
        get_walls(maze, 1, 5)

    with pytest.raises(TypeError):
        get_walls([[[True, False, "Not a bool", False]]], 0, 0)
