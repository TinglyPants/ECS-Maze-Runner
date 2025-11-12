# Copyright (c) 2025 Matty Chalk
# Licensed under the MIT License (see LICENSE file for details)

"""Module defining functions related to the maze."""

from direction import Direction
from turn import Turn

def create_maze(width: int = 5, height: int = 5) -> list[list[tuple[bool, bool, bool, bool]]]:
    """Return a 2D list of tuples representing a generated maze.

    Each cell in the maze is represented by a tuple with 4 boolean values to indicate the presence of walls.
    Indexing the tuple should be done by casting a `Direction` to an int.
    A value of `True` implies a wall is present.

    Parameters
    ----------
    width : int, optional
        The width of the maze generated. Default is 5.
    height : int, optional
        The height of the maze generated. Default is 5.

    Returns
    -------
    list[list[tuple[bool, bool, bool, bool]]]
        The 2D list of tuples representing a generated maze.
        The cell at position (x,y) should be accessed as such: maze[x][y]
    """
    # Initially, a maze with no external walls is generated. Cells are accessed by generated_maze[x][y].
    generated_maze = [[(False, False, False, False) for _ in range(height)] for _ in range(width)]