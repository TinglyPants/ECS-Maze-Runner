# Copyright (c) 2025 Matty Chalk
# Licensed under the MIT License (see LICENSE file for details)

"""Module defining functions related to maze runners."""

from src.direction import Direction
from src.turn import Turn


def create_runner(
    x: int = 0, y: int = 0, orientation: Direction = Direction.NORTH
) -> dict:
    """Return a dictionary object representing a maze runner.

    Parameters
    ----------
    x : int, optional
        The X coordinate the runner starts at. Default is 0.
    y : int, optional
        The Y coordinate the runner starts at. Default is 0.
    orientation : `Direction`, optional
        The starting orientation of the runner. Must be a member of the `Direction` enum. Default is `NORTH`.

    Returns
    -------
    dict
        A dictionary object representing a maze runner.
    """
    if not isinstance(x, int):
        raise TypeError(f"x must be int, got {type(x).__name__}")
    if not isinstance(y, int):
        raise TypeError(f"y must be int, got {type(y).__name__}")
    if not isinstance(orientation, Direction):
        raise TypeError(
            f"orientation must be Direction enum member, got {type(orientation).__name__}"
        )

    return {"x": x, "y": y, "orientation": orientation}


def get_x(runner: dict) -> int:
    """Return the X coordinate of the runner.

    Parameters
    ----------
    runner : dict
        The dictionary object representing a maze runner.

    Returns
    -------
    int
        The x coordinate of the runner.
    """
    if not isinstance(runner, dict):
        raise TypeError(f"runner must be dict, got {type(runner).__name__}")
    if "x" not in runner:
        raise KeyError(f"runner must contain the 'x' key")
    if not isinstance(runner["x"], int):
        raise TypeError(f"'x' must be int, got {type(runner['x']).__name__}")

    return runner["x"]


def get_y(runner: dict) -> int:
    """Return the Y coordinate of the runner.

    Parameters
    ----------
    runner : dict
        The dictionary object representing a maze runner.

    Returns
    -------
    int
        The y coordinate of the runner.
    """
    if not isinstance(runner, dict):
        raise TypeError(f"runner must be dict, got {type(runner).__name__}")
    if "y" not in runner:
        raise KeyError(f"runner must contain the 'y' key")
    if not isinstance(runner["y"], int):
        raise TypeError(f"'y' must be int, got {type(runner['y']).__name__}")

    return runner["y"]


def get_orientation(runner: dict) -> Direction:
    """Return the orientation of the runner.

    Parameters
    ----------
    runner : dict
        The dictionary object representing a maze runner.

    Returns
    -------
    `Direction`
        The orientation of the runner.
    """
    if not isinstance(runner, dict):
        raise TypeError(f"runner must be dict, got {type(runner).__name__}")
    if "orientation" not in runner:
        raise KeyError(f"runner must contain the 'orientation' key")
    if not isinstance(runner["orientation"], Direction):
        raise TypeError(
            f"'orientation' must be Direction enum member, got {type(runner['orientation']).__name__}"
        )

    return runner["orientation"]


def turn(runner: dict, direction: Turn) -> dict:
    """Turn the runner a given direction, then return the turned runner.

    Parameters
    ----------
    runner : dict
        The dictionary object representing a maze runner.
    direction : Turn
        The direction to turn the runner. Must be a member of the `Turn` enum.

    Returns
    -------
    dict
        A dictionary object representing the turned runner.
    """
    orientation = get_orientation(runner)
    if not isinstance(direction, Turn):
        raise TypeError(
            f"direction must be Turn enum member, got {type(direction).__name__}"
        )

    if direction == Turn.RIGHT:
        return {**runner, "orientation": orientation.turn_right()}
    else:  # direction can only == Turn.LEFT
        return {**runner, "orientation": orientation.turn_left()}


def forward(runner: dict) -> dict:
    """Move the runner forward one cell, then return the moved runner.

    Parameters
    ----------
    runner : dict
        The dictionary object representing a maze runner.

    Returns
    -------
    dict
        A dictionary object representing the moved runner.
    """
    x = get_x(runner)
    y = get_y(runner)
    orientation = get_orientation(runner)

    match orientation:
        case Direction.NORTH:
            y += 1
        case Direction.EAST:
            x += 1
        case Direction.SOUTH:
            y -= 1
        case Direction.WEST:
            x -= 1

    return {**runner, "x": x, "y": y}
