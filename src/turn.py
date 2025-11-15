# Copyright (c) 2025 Matty Chalk
# Licensed under the MIT License (see LICENSE file for details)

"""Module defining the Turn enum for turning directions."""

from enum import Enum


class Turn(Enum):
    """Enumeration of the turning directions.

    Members
    -------
    LEFT : str = "Left"
    RIGHT : str = "Right"
    """

    LEFT = "Left"
    RIGHT = "Right"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Turn):
            return self.value == other.value
        if isinstance(other, str):
            return self.value == other
        raise NotImplementedError
