# Copyright (c) 2025 Matty Chalk
# Licensed under the MIT License (see LICENSE file for details)

"""Testing module for runner.py."""

import pytest
from runner import *
from direction import Direction
from turn import Turn


def test_create_runner_assignment():
    """Unit test create_runner assignment."""
    assert create_runner() == {"x": 0, "y": 0, "orientation": Direction.NORTH}
    assert create_runner(x=1, y=1, orientation=Direction.EAST) == {
        "x": 1,
        "y": 1,
        "orientation": Direction.EAST,
    }
    assert create_runner(5, 7, Direction.WEST) == {
        "x": 5,
        "y": 7,
        "orientation": Direction.WEST,
    }


def test_create_runner_type_validation():
    """Unit test create_runner type validation."""
    with pytest.raises(TypeError):
        create_runner(x="Not an integer")
    with pytest.raises(TypeError):
        create_runner(y="Not an integer")
    with pytest.raises(TypeError):
        create_runner(orientation="Not a Direction enum")


def test_get_x():
    """Unit test get_x."""
    runner = create_runner(1, 2, Direction.SOUTH)
    assert get_x(runner) == 1


def test_get_x_type_validation():
    """Unit test get_x type validation."""
    runner = "Not a dict"
    with pytest.raises(TypeError):
        get_x(runner)

    runner = {"A": "Missing x key"}
    with pytest.raises(KeyError):
        get_x(runner)

    runner = create_runner(1, 2, Direction.SOUTH)
    runner["x"] = "Not an integer"
    with pytest.raises(TypeError):
        get_x(runner)


def test_get_y():
    """Unit test get_y."""
    runner = create_runner(1, 2, Direction.SOUTH)
    assert get_y(runner) == 2


def test_get_y_type_validation():
    """Unit test get_y type validation."""
    runner = "Not a dict"
    with pytest.raises(TypeError):
        get_y(runner)

    runner = {"A": "Missing y key"}
    with pytest.raises(KeyError):
        get_y(runner)

    runner = create_runner(1, 2, Direction.SOUTH)
    runner["y"] = "Not an integer"
    with pytest.raises(TypeError):
        get_y(runner)


def test_get_orientation():
    """Unit test get_orientation."""
    runner = create_runner(1, 2, Direction.SOUTH)
    assert get_orientation(runner) == Direction.SOUTH


def test_get_orientation_type_validation():
    """Unit test get_orientation type validation."""
    runner = "Not a dict"
    with pytest.raises(TypeError):
        get_orientation(runner)

    runner = {"A": "Missing orientation key"}
    with pytest.raises(KeyError):
        get_orientation(runner)

    runner = create_runner(1, 2, Direction.SOUTH)
    runner["orientation"] = "Not a Direction enum"
    with pytest.raises(TypeError):
        get_orientation(runner)


def test_turn():
    """Unit test turn."""
    runner = create_runner(1, 2, Direction.SOUTH)
    assert turn(runner, Turn.RIGHT)["orientation"] == Direction.WEST
    assert turn(runner, Turn.LEFT)["orientation"] == Direction.EAST


def test_turn_type_validation():
    """Unit test turn type validation."""
    runner = create_runner(1, 2, Direction.SOUTH)
    with pytest.raises(TypeError):
        turn(runner, "Not a Turn enum")


def test_forward():
    """Unit test forward."""
    runner_north = create_runner(0, 0, Direction.NORTH)
    runner_east = create_runner(0, 0, Direction.EAST)
    runner_south = create_runner(0, 0, Direction.SOUTH)
    runner_west = create_runner(0, 0, Direction.WEST)

    assert forward(runner_north) == {"x": 0, "y": 1, "orientation": Direction.NORTH}
    assert forward(runner_east) == {"x": 1, "y": 0, "orientation": Direction.EAST}
    assert forward(runner_south) == {"x": 0, "y": -1, "orientation": Direction.SOUTH}
    assert forward(runner_west) == {"x": -1, "y": 0, "orientation": Direction.WEST}
