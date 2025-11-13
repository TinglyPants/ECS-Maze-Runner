# Copyright (c) 2025 Matty Chalk
# Licensed under the MIT License (see LICENSE file for details)

"""Module defining the Wall enum for wall directions."""

from enum import Enum


class Wall(Enum):
    """Enumeration of the wall directions.

    Members
    -------
    LEFT : int = 0
    FORWARD : int = 1
    RIGHT : int = 2
    """

    LEFT = 0
    FORWARD = 1
    RIGHT = 2

    def __int__(self) -> int:
        return self.value
