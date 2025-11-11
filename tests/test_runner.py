# Copyright (c) 2025 Matty Chalk
# Licensed under the MIT License (see LICENSE file for details)

"""Testing module for runner.py."""

import pytest
from runner import *
from direction import Direction
from turn import Turn

def test_create_runner_assignment():
    assert create_runner() == {'x': 0, 'y': 0, 'orientation': Direction.NORTH}
    assert create_runner(x=1, y=1, orientation=Direction.EAST) == {'x': 1, 'y': 1, 'orientation': Direction.EAST}
    assert create_runner(5, 7, Direction.WEST) == {'x': 5, 'y': 7, 'orientation': Direction.WEST}


def test_create_runner_type_validation():
    with pytest.raises(TypeError):
        create_runner(x="Not an integer")
    with pytest.raises(TypeError):
        create_runner(y="Not an integer")
    with pytest.raises(TypeError):
        create_runner(orientation="Not a Direction enum")