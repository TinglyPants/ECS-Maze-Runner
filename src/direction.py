# Copyright (c) 2025 Matty Chalk
# Licensed under the MIT License (see LICENSE file for details)

"""Module defining the Direction enum for cardinal directions."""

from __future__ import annotations
from enum import Enum


class Direction(Enum):
    """Enumeration of the cardinal directions.

    Members
    -------
    NORTH : str = "N"
    EAST : str = "E"
    SOUTH : str = "S"
    WEST : str = "W"
    """

    NORTH = "N"
    EAST = "E"
    SOUTH = "S"
    WEST = "W"

    def turn_right(self) -> Direction:
        """Return the `Direction` 90 degrees clockwise.

        Returns
        -------
        `Direction`
            The `Direction` 90 degrees clockwise.
        """
        order: list = [Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST]
        index: int = order.index(Direction(self.value))
        return Direction(order[(index + 1) % 4])

    def turn_left(self) -> Direction:
        """Return the `Direction` 90 degrees anti-clockwise.

        Returns
        -------
        `Direction`
            The `Direction` 90 degrees anti-clockwise.
        """
        order: list = [Direction.NORTH, Direction.WEST, Direction.SOUTH, Direction.EAST]
        index: int = order.index(Direction(self.value))
        return Direction(order[(index + 1) % 4])

    def __int__(self) -> int:
        """Return the integer representation of the `Direction`

        The cardinal directions are assigned a 0 indexed integer, increasing clockwise starting from NORTH.
        NORTH -> 0,
        EAST -> 1,
        SOUTH -> 2,
        WEST -> 3.

        Returns
        -------
        int
            The integer representation of the `Direction`.
        """
        match self:
            case Direction.NORTH:
                return 0
            case Direction.EAST:
                return 1
            case Direction.SOUTH:
                return 2
            case Direction.WEST:
                return 3
