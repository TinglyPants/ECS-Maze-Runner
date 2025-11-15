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
    """Removes duplicate positions from the linked path and returns a normal path.

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

def _construct_sequences(optimised_path: list[tuple[int, int, str]], starting_direction: Direction) -> list[tuple[int, int, str]]:
    """Adds sequences to the optimised path, as well as removing the last (goal) position.

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

def shortest_path(maze: list[list[list[bool]]], starting: tuple[int, int] | None = None, goal: tuple[int, int] | None = None) -> list[tuple[int, int, str]]:
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

    Returns
    -------
    list[tuple[int, int, str]]
        The shortest sequence from the starting position to the goal position found by a maze runner.
    """
    starting_x, starting_y = get_position_or_default(maze, starting, (Direction.WEST, Direction.SOUTH))
    runner = create_runner(starting_x, starting_y)
    path = explore(runner, maze, goal)

    linked_path = link_list(path)
    optimised_path = _optimise_path(linked_path)
    optimised_path_with_sequences = _construct_sequences(optimised_path, Direction.NORTH)

    return optimised_path_with_sequences
