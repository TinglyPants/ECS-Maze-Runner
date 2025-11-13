# Copyright (c) 2025 Matty Chalk
# Licensed under the MIT License (see LICENSE file for details)

"""Module defining functions related to maze runners."""

from direction import Direction
from turn import Turn
from wall import Wall
from maze import get_walls, get_dimensions

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


def backward(runner: dict) -> dict:
    """Move the runner backward one cell, then return the moved runner.

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
            y -= 1
        case Direction.EAST:
            x -= 1
        case Direction.SOUTH:
            y += 1
        case Direction.WEST:
            x += 1

    return {**runner, "x": x, "y": y}


def sense_walls(runner: dict, maze: list[list[list[bool]]]) -> tuple[bool, bool, bool]:
    """Return a tuple indicating whether there are walls to the left, straight ahead, or to the right of the runner.

    The returned tuple has the order: left, straight, right.
    Indexing the tuple should be done by casting a `Wall` enum to an int.
    A value of `True` indicates that a wall is present.

    Parameters
    ----------
    runner : dict
        The dictionary object representing a maze runner.
    maze : list[list[list[bool]]]
        The maze the runner is in.

    Returns
    -------
    tuple[bool, bool, bool]
        The tuple indicating whether there are walls to the left, straight ahead, or to the right of the runner.
    """
    x = get_x(runner)
    y = get_y(runner)
    cell = get_walls(maze, x, y)

    # Get left and right of runner
    orientation = get_orientation(runner)
    left_direction = orientation.turn_left()
    right_direction = orientation.turn_right()

    return cell[int(left_direction)], cell[int(orientation)], cell[int(right_direction)]


def go_straight(runner: dict, maze: list[list[list[bool]]]) -> dict:
    """Advance the runner straight by one position, then return the moved runner.

    If the runner attempts to walk through a wall, a ValueError is raised.

    Parameters
    ----------
    runner : dict
        The dictionary object representing a maze runner.
    maze : list[list[list[bool]]]
        The maze the runner is in.

    Returns
    -------
    dict
        A dictionary object representing the moved runner.
    """
    if not sense_walls(runner, maze)[1]: # Wall directly ahead is empty
        return forward(runner)
    else:
        raise ValueError("runner cannot walk through a wall")


def move(runner: dict, maze: list[list[list[bool]]]) -> tuple[dict, str]:
    """Move the runner by one cell, then return the moved runner and the sequence of actions taken to get there.

    The runner will use a simple left-hug algorithm to move the runner. Each call of the function will advance the runner by one cell.
    The sequence of actions returned uses "L" and "R" to indicate left and right turns respectively.
    The sequence of actions returned uses "F" and "B" to indicate forward and backward movements respectively.

    Parameters
    ----------
    runner : dict
        The dictionary object representing a maze runner.
    maze : list[list[list[bool]]]
        The maze the runner is in.

    Returns
    -------
    tuple[dict, str]
        A tuple containing the moved runner and the sequence of actions taken to get there.
    """
    walls = sense_walls(runner, maze)
    sequence = ""

    if not walls[int(Wall.LEFT)]:
        # Go left
        sequence += "LF"
        runner = turn(runner, Turn.LEFT)
        runner = forward(runner)
    elif not walls[int(Wall.FORWARD)]:
        # Go forward
        sequence += "F"
        runner = forward(runner)
    elif not walls[int(Wall.RIGHT)]:
        # Go right
        sequence += "RF"
        runner = turn(runner, Turn.RIGHT)
        runner = forward(runner)
    else:
        # Go back
        sequence += "B"
        runner = backward(runner)

    return runner, sequence


def in_goal(runner: dict, goal_x: int, goal_y: int) -> bool:
    """Return whether the runner is in the goal position.

    Parameters
    ----------
    runner : dict
        The dictionary object representing a maze runner.
    goal_x : int
        The x position of the goal.
    goal_y : int
        The y position of the goal.

    Returns
    -------
    bool
        Whether the runner is in the goal position.
    """
    x = get_x(runner)
    y = get_y(runner)

    return (x == goal_x) and (y == goal_y)

def explore(runner: dict, maze: list[list[list[bool]]], goal: tuple[int, int] | None = None) -> list[tuple[int, int, str]]:
    """Advance the runner through the maze until the goal is reached. Return the sequence of positions and actions taken to get there.

    Parameters
    ----------
    runner : dict
        The dictionary object representing a maze runner.
    maze : list[list[list[bool]]]
        The maze the runner is in.
    goal : tuple[int, int], optional
        The position of the goal. If None, the goal will be the top right of the maze. Default is None.

    Returns
    -------
    list[tuple[int, int, str]]
        The sequence of positions and actions taken to get to the goal.
    """
    # Get goal position
    goal_x, goal_y = None, None
    width, height = get_dimensions(maze)
    if goal is None:
        goal_x = width - 1
        goal_y = height - 1
    else:
        if not isinstance(goal, tuple):
            raise TypeError(f"goal must be a tuple, got {type(goal).__name__}")
        if not (isinstance(goal[0], int) and isinstance(goal[1], int)):
            raise TypeError(f"goal must be be tuple (int, int), got ({type(goal[0]).__name__}, {type(goal[1]).__name__})")

        goal_x, goal_y = goal

        if goal_x >= width or goal_y >= height or goal_x < 0 or goal_y < 0:
            raise ValueError(f"goal must be inside the maze, got ({goal_x}, {goal_y})")

    # Move runner until runner is at the goal
    runner_action_sequence = []
    while not in_goal(runner, goal_x, goal_y):
        runner, action = move(runner, maze)
        runner_action_sequence.append((get_x(runner), get_y(runner), action))

    return runner_action_sequence