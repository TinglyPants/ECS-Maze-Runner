# Copyright (c) 2025 Matty Chalk
# Licensed under the MIT License (see LICENSE file for details)

"""Testing module for direction.py."""

from direction import Direction


def test_turn_left():
    """Unit test turn_left."""
    assert Direction.NORTH.turn_left() == Direction.WEST
    assert Direction.EAST.turn_left() == Direction.NORTH
    assert Direction.SOUTH.turn_left() == Direction.EAST
    assert Direction.WEST.turn_left() == Direction.SOUTH


def test_turn_right():
    """Unit test turn_right."""
    assert Direction.NORTH.turn_right() == Direction.EAST
    assert Direction.EAST.turn_right() == Direction.SOUTH
    assert Direction.SOUTH.turn_right() == Direction.WEST
    assert Direction.WEST.turn_right() == Direction.NORTH


def test_int():
    """Unit test __int__ conversion"""
    assert int(Direction.NORTH) == 0
    assert int(Direction.EAST) == 1
    assert int(Direction.SOUTH) == 2
    assert int(Direction.WEST) == 3
