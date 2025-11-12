# Copyright (c) 2025 Matty Chalk
# Licensed under the MIT License (see LICENSE file for details)

"""Module defining functions related to the maze."""

from direction import Direction
from turn import Turn

def create_maze(width: int = 5, height: int = 5) -> list[list[list[bool]]]:
    """Return a 2D list of cells representing a generated maze.

    Each cell in the maze is represented by a list with 4 boolean values to indicate the presence of walls.
    Indexing the cell should be done by casting a `Direction` to an int.
    A value of `True` implies a wall is present.

    Parameters
    ----------
    width : int, optional
        The width of the maze generated. Default is 5.
    height : int, optional
        The height of the maze generated. Default is 5.

    Returns
    -------
    list[list[list[bool]]]
        The 2D list of cells representing a generated maze.
        The cell at position (x,y) should be accessed as such: maze[x][y]
    """
    if not isinstance(width, int):
        raise TypeError(f"width must be int, got {type(width).__name__}")
    if not isinstance(height, int):
        raise TypeError(f"height must be int, got {type(height).__name__}")
    if width <= 0:
        raise ValueError(f"width must be greater than 0, got {width}")
    if height <= 0:
        raise ValueError(f"height must be greater than 0, got {height}")

    # Initially, a maze with no external walls is generated. Cells are accessed by generated_maze[x][y].
    generated_maze = [[[False, False, False, False] for _ in range(height)] for _ in range(width)]

    # Generating external walls
    for i in range(width):
        for j in range(height):
            # Co-ordinate is (i, j).
            if i == 0:
                generated_maze[i][j][int(Direction.WEST)] = True # Set west wall
            if i == width - 1:
                generated_maze[i][j][int(Direction.EAST)] = True # Set east wall
            if j == 0:
                generated_maze[i][j][int(Direction.SOUTH)] = True # Set south wall
            if j == height - 1:
                generated_maze[i][j][int(Direction.NORTH)] = True # Set north wall

    return generated_maze


def add_horizontal_wall(maze: list[list[list[bool]]], x_coordinate: int, horizontal_line: int) -> list[list[list[bool]]]:
    """Return the maze with a horizontal wall added.

    Attempting to add a horizontal wall to the edges of the maze will result in a ValueError.

    Parameters
    ----------
    maze : list[list[list[bool]]]
        The maze to add horizontal wall to.
    x_coordinate : int
        The x coordinate of the wall.
    horizontal_line : int
        The horizontal line position of the wall.

    Returns
    -------
    list[list[list[bool]]]
        The maze with a horizontal wall added.
    """
    if not isinstance(x_coordinate, int):
        raise TypeError(f"x_coordinate must be int, got {type(x_coordinate).__name__}")
    if not isinstance(horizontal_line, int):
        raise TypeError(f"horizontal_line must be int, got {type(horizontal_line).__name__}")
    if x_coordinate < 0:
        raise ValueError(f"x_coordinate must be greater than or equal to 0, got {x_coordinate}")
    if horizontal_line < 0:
        raise ValueError(f"horizontal_line must be greater than or equal to 0, got {horizontal_line}")

    width, height = get_dimensions(maze)

    if x_coordinate >= width:
        raise ValueError(f"x_coordinate must be less than width ({width}), got {x_coordinate}")
    if horizontal_line == 0 or horizontal_line == height:
        raise ValueError(f"cannot add a horizontal wall to the edge of the maze.")

    # Horizontal wall affects adjacent cells at indices [horizontal_line] and [horizontal_line - 1].
    maze[x_coordinate][horizontal_line][int(Direction.SOUTH)] = True # Set south wall
    maze[x_coordinate][horizontal_line - 1][int(Direction.NORTH)] = True # Set north wall

    return maze

def add_vertical_wall(maze: list[list[list[bool]]], y_coordinate: int, vertical_line: int) -> list[list[list[bool]]]:
    pass

def get_dimensions(maze: list[list[list[bool]]]) -> tuple[int, int]:
    """Return the dimensions of the maze.

    Parameters
    ----------
    maze : list[list[list[bool]]]
        The maze to get dimensions from.

    Returns
    -------
    tuple[int, int]
        The dimensions of the maze.
        Returned as (width, height).
    """
    if not (isinstance(maze, list) and isinstance(maze[0], list)):
        raise TypeError(f"maze must be list[list]!")

    width = len(maze)
    height = len(maze[0])

    # Ensure maze is not jagged
    for column in maze:
        if len(column) != height:
            raise ValueError(f"maze list[list] must not be jagged!")

    return width, height

def get_walls(maze: list[list[list[bool]]], x_coordinate: int, y_coordinate: int) -> tuple[bool, bool, bool, bool]:
    """Return the cell at a given position in the maze.

    Each cell in the maze is represented by a list with 4 boolean values to indicate the presence of walls.
    Indexing the cell should be done by casting a `Direction` to an int.
    A value of `True` implies a wall is present.

    Parameters
    ----------
    maze : list[list[list[bool]]]
        The maze to search for cells.
    x_coordinate : int
        The x coordinate of the cell.
    y_coordinate : int
        The y coordinate of the cell.

    Returns
    -------
    tuple[bool, bool, bool, bool]
        The cell at a given position in the maze.
    """
    if not isinstance(x_coordinate, int):
        raise TypeError(f"x_coordinate must be int, got {type(x_coordinate).__name__}")
    if not isinstance(y_coordinate, int):
        raise TypeError(f"y_coordinate must be int, got {type(y_coordinate).__name__}")
    if x_coordinate < 0:
        raise ValueError(f"x_coordinate must be greater than or equal to 0, got {x_coordinate}")
    if y_coordinate < 0:
        raise ValueError(f"y_coordinate must be greater than or equal to 0, got {y_coordinate}")

    width, height = get_dimensions(maze)

    if x_coordinate >= width:
        raise ValueError(f"x_coordinate must be less than width ({width}), got {x_coordinate}")
    if y_coordinate >= height:
        raise ValueError(f"y_coordinate must be less than height ({height}), got {y_coordinate}")

    cell = maze[x_coordinate][y_coordinate]

    if not (isinstance(cell, list) and isinstance(cell[0], bool)):
        raise TypeError(f"maze cell must be list[bool]!")

    return cell[0], cell[1], cell[2], cell[3]