# Copyright (c) 2025 Matty Chalk
# Licensed under the MIT License (see LICENSE file for details)

"""Module defining behaviour related to both the maze and the runner combined."""

from runner import *
from maze import *


def link_list(list_to_link: list) -> list[list]:
    """Return a linked list from a supplied list.

    Parameters
    ----------
    list_to_link: list[list]
        The list to link.

    Returns
    -------
    list[list]
        The newly linked list.
    """
    linked_list = [[item, index + 1] for index, item in enumerate(list_to_link)]
    linked_list[-1][1] = -1  # Set last link to -1 to indicate end of linked list
    return linked_list


def _optimise_path(linked_path: list[list]) -> list[tuple[int, int, str]]:
    """Remove duplicate positions from the linked path and return a normal path.

    This is an internal helper method - not intended to be called externally.

    Parameters
    ----------
    linked_path: list[list]
        The linked path to remove duplicate positions from.

    Returns
    -------
    list[tuple[int, int, str]]
        The new, non-linked path. The string part of the tuple will be empty, to be filled in later.
    """
    # Remove unnecessary positions from linked path by reassigning pointers
    seen_positions: dict[tuple[int, int], int] = {}
    for index, ((pos_x, pos_y, _), next_index) in enumerate(linked_path):
        # End of journey, skip iteration
        if next_index == -1:
            continue

        if (pos_x, pos_y) in seen_positions:
            index_of_previously_seen = seen_positions[(pos_x, pos_y)]
            # Skip all the unnecessary positions in between
            linked_path[index_of_previously_seen][1] = next_index
            # Update seen_positions
            seen_positions[(pos_x, pos_y)] = index
        else:
            seen_positions[(pos_x, pos_y)] = index

    optimised_path: list[tuple[int, int, str]] = []
    # Iterate through linked path, using the links to get the optimised path
    next_index = 0
    while next_index != -1:
        pos_x = linked_path[next_index][0][0]
        pos_y = linked_path[next_index][0][1]
        optimised_path.append((pos_x, pos_y, ""))

        next_index = linked_path[next_index][1]

    return optimised_path


def _construct_sequences(
    optimised_path: list[tuple[int, int, str]], starting_direction: Direction
) -> list[tuple[int, int, str]]:
    """Add sequences to the optimised path, as well as removing the last (goal) position.

    This is an internal helper method - not intended to be called externally.

    Parameters
    ----------
    optimised_path: list[tuple[int, int, str]]
        The optimised path to add sequences to.
    starting_direction: Direction
        The `Direction` the runner started out facing.

    Returns
    -------
    list[tuple[int, int, str]]
        The optimised path with sequences added. The last item is also removed.
    """
    prev_direction = starting_direction
    for index, (pos_x, pos_y, sequence) in enumerate(optimised_path[:-1]):
        next_index = index + 1
        next_pos_x = optimised_path[next_index][0]
        next_pos_y = optimised_path[next_index][1]
        left_direction = prev_direction.turn_left()
        right_direction = prev_direction.turn_right()

        movement_direction = None
        if next_pos_x > pos_x:
            movement_direction = Direction.EAST
        elif next_pos_x < pos_x:
            movement_direction = Direction.WEST
        elif next_pos_y > pos_y:
            movement_direction = Direction.NORTH
        elif next_pos_y < pos_y:
            movement_direction = Direction.SOUTH

        if movement_direction == prev_direction:
            optimised_path[index] = (pos_x, pos_y, "F")
        elif movement_direction == left_direction:
            optimised_path[index] = (pos_x, pos_y, "LF")
        elif movement_direction == right_direction:
            optimised_path[index] = (pos_x, pos_y, "RF")
        else:
            optimised_path[index] = (pos_x, pos_y, "B")

        prev_direction = movement_direction

    return optimised_path[:-1]


def write_exploration_path_to_file(
    path: list[tuple[int, int, str]], exploration_file: str
) -> None:
    """Write the exploration path to a file."""
    with open(exploration_file, "w") as file:
        file.write("Step,x-coordinate,y-coordinate,Actions\n")
        for index, (pos_x, pos_y, sequence) in enumerate(path[:-1]):
            file.write(f"{index+1},{pos_x},{pos_y},{path[index+1][2]}\n")


def write_statistics_to_file(
    maze_file: str | None,
    exploration_path: list[tuple[int, int, str]],
    optimised_path: list[tuple[int, int, str]],
    statistics_file: str,
) -> None:
    """Write the statistics to a file"""
    with open(statistics_file, "w") as file:
        file.write(f"{maze_file}\n")
        exploration_steps = len(exploration_path) - 1
        path_length = len(optimised_path) + 1
        score = exploration_steps / 4 + path_length
        file.write(f"{score}\n")
        file.write(f"{exploration_steps}\n")
        file.write(f"{optimised_path}\n")
        file.write(f"{path_length}")


def shortest_path(
    maze: list[list[list[bool]]],
    starting: tuple[int, int] | None = None,
    goal: tuple[int, int] | None = None,
    scribe: bool = False,
    maze_file_name: str | None = None,
) -> list[tuple[int, int, str]]:
    """Return the shortest sequence from the starting position to the goal position found by a maze runner.

    The path found may not necessarily be the shortest possible, as that is determined by the exploration algorithm.

    Parameters
    ----------
    maze: list[list[list[bool]]]
        The maze to explore.
    starting: tuple[int, int], optional
        The starting position of the runner. If None, the starting position will be the bottom left of the maze. Default is None.
    goal : tuple[int, int], optional
        The position of the goal. If None, the goal will be the top right of the maze. Default is None.
    scribe : bool, optional
        Set to `True` to have actions be recorded to a file.
    maze_file_name: str, optional
        Set to a string to record the name of the maze file when scribing. Default is None.

    Returns
    -------
    list[tuple[int, int, str]]
        The shortest sequence from the starting position to the goal position found by a maze runner.
    """
    if not isinstance(scribe, bool):
        raise TypeError(f"scribe must be bool, got {type(scribe).__name__}")

    starting_x, starting_y = get_position_or_default(
        maze, starting, (Direction.WEST, Direction.SOUTH)
    )
    runner = create_runner(starting_x, starting_y)
    path = explore(runner, maze, goal)

    linked_path = link_list(path)
    optimised_path = _optimise_path(linked_path)
    optimised_path_with_sequences = _construct_sequences(
        optimised_path, Direction.NORTH
    )

    if scribe:
        write_exploration_path_to_file(path, "exploration.csv")
        write_statistics_to_file(
            maze_file_name, path, optimised_path_with_sequences, "statistics.txt"
        )

    return optimised_path_with_sequences


def is_valid_maze_file(maze_file: str) -> bool:
    """Return `True` if `maze_file` is a valid maze file.

    Parameters
    ----------
    maze_file: str
        The path to the maze file.

    Returns
    -------
    bool
    `True` if `maze_file` is a valid maze file.
    """
    with open(maze_file, "r") as file:
        maze_file_lines = [line.strip() for line in file.readlines()]

        # Ensure all lines are same length
        length = len(maze_file_lines[0])
        for line in maze_file_lines:
            if len(line) != length:
                return False

        # Ensure line length and line count are odd
        if len(maze_file_lines) % 2 == 0:
            return False
        if len(maze_file_lines[0]) % 2 == 0:
            return False

        # Ensure external walls present
        for char in maze_file_lines[0] + maze_file_lines[-1]:
            if char != "#":
                return False
        for line in maze_file_lines[1:-1]:
            if line[0] != "#" or line[-1] != "#":
                return False

        # Ensure wall intersections are all hashes
        for line in maze_file_lines[0::2]:
            for char in line[0::2]:
                if char != "#":
                    return False

        # Ensure cell positions are all dots
        for line in maze_file_lines[1::2]:
            for char in line[1::2]:
                if char != ".":
                    return False

    return True


def get_maze_file_dimensions(maze_file: str) -> tuple[int, int]:
    """Return the dimensions of the maze file as (width, height).

    Parameters
    ----------
    maze_file: str
        The path to the maze file.

    Returns
    -------
    tuple[int, int]
        The dimensions of the maze file as (width, height).
    """
    with open(maze_file, "r") as file:
        maze_file_lines = [line.strip() for line in file.readlines()]

        maze_width: int = (len(maze_file_lines[0]) - 1) // 2
        maze_height: int = (len(maze_file_lines) - 1) // 2

        return maze_width, maze_height


def get_maze_file_cells(maze_file: str) -> list[list[tuple[str, str, str, str]]]:
    """Return the cells of the maze file, where each cell is a tuple of 4 characters.

    Each cell tuple represents the 4 neighbouring characters to that cell.
    The tuple should be indexed by casting a `Direction` enum to an integer.

    Parameters
    ----------
    maze_file: str
        The path to the maze file.

    Returns
    -------
    list[list[tuple[str, str, str, str]]]
        The cells of the maze file.
    """
    cells: list[list[tuple[str, str, str, str]]] = None
    with open(maze_file, "r") as file:
        maze_file_lines = [line.strip() for line in file.readlines()]

        maze_width, maze_height = get_maze_file_dimensions(maze_file)

        # cells indexed as cells[x][y]
        cells = [
            [("", "", "", "") for _ in range(maze_height)] for _ in range(maze_width)
        ]

        for line_index, line in enumerate(maze_file_lines):
            for char_index, char in enumerate(line):
                if line_index % 2 == 1 and char_index % 2 == 1:
                    cell_x: int = (char_index - 1) // 2
                    cell_y: int = (len(maze_file_lines) - line_index - 2) // 2

                    north_neighbour = maze_file_lines[line_index - 1][char_index]
                    east_neighbour = maze_file_lines[line_index][char_index + 1]
                    south_neighbour = maze_file_lines[line_index + 1][char_index]
                    west_neighbour = maze_file_lines[line_index][char_index - 1]

                    cells[cell_x][cell_y] = (
                        north_neighbour,
                        east_neighbour,
                        south_neighbour,
                        west_neighbour,
                    )

    return cells


def maze_file_cell_to_maze_cell(
    maze_file_cell: tuple[str, str, str, str],
) -> list[bool]:
    """Read a maze file cell and convert it to a regular maze cell.

    Parameters
    ----------
    maze_file_cell: tuple[str, str, str, str]
        The maze file cell.

    Returns
    -------
    list[bool]
        The maze file cell converted to a regular maze cell.
    """
    maze_cell = [False, False, False, False]
    maze_cell[int(Direction.NORTH)] = maze_file_cell[int(Direction.NORTH)] == "#"
    maze_cell[int(Direction.EAST)] = maze_file_cell[int(Direction.EAST)] == "#"
    maze_cell[int(Direction.SOUTH)] = maze_file_cell[int(Direction.SOUTH)] == "#"
    maze_cell[int(Direction.WEST)] = maze_file_cell[int(Direction.WEST)] == "#"

    return maze_cell


def maze_reader(maze_file: str) -> list[list[list[bool]]]:
    """Read a maze file to build a maze, then return that maze.

    Parameters
    ----------
    maze_file: str
        The path to the maze file.

    Returns
    -------
    list[list[list[bool]]]
        The maze created.
    """
    try:
        if not is_valid_maze_file(maze_file):
            raise ValueError("maze file must contain a valid maze.")

        maze_file_cells = get_maze_file_cells(maze_file)
        maze_width, maze_height = get_maze_file_dimensions(maze_file)
        maze = create_maze(maze_width, maze_height)

        for i in range(maze_width):
            for j in range(maze_height):
                maze[i][j] = maze_file_cell_to_maze_cell(maze_file_cells[i][j])

        return maze
    except ValueError:
        raise
    except:
        raise IOError("there was an issue reading from the maze file.")
