# Copyright (c) 2025 Matty Chalk
# Licensed under the MIT License (see LICENSE file for details)

"""Module defining behaviour related to both the maze and the runner combined."""

from runner import *
from maze import *

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
    path_explored = explore(runner, maze, goal)

    # Convert explored path to linked list of positions.
    linked_path_explored = [[(pos_x, pos_y), index + 1] for index, (pos_x, pos_y, sequence) in enumerate(path_explored)]
    linked_path_explored[-1][1] = -1  # Set last pointer to -1 to indicate end of linked list

    # Iterate through linked list of positions, recording positions seen and where in the list they were seen.
    # When a duplicate position is found, restructure the linked list to remove the unnecessary steps between. Then, update the stored positions
    seen_positions: dict[tuple[int, int], int] = {}
    for index, ((pos_x, pos_y), next_index) in enumerate(linked_path_explored):
        # End of journey, skip iteration
        if next_index == -1:
            continue

        if (pos_x, pos_y) in seen_positions:
            index_of_previously_seen = seen_positions[(pos_x, pos_y)]
            # Skip all the unnecessary positions in between
            linked_path_explored[index_of_previously_seen][1] = next_index
            # Update seen_positions
            seen_positions[(pos_x, pos_y)] = index
        else:
            seen_positions[(pos_x, pos_y)] = index

    optimised_path: list[tuple[int, int, str]] = []
    # Iterate through linked list of positions, using the links to get the optimised path
    next_index = 0
    while next_index != -1:
        pos_x = linked_path_explored[next_index][0][0]
        pos_y = linked_path_explored[next_index][0][1]
        optimised_path.append((pos_x, pos_y, ""))

        next_index = linked_path_explored[next_index][1]

    # Iterate through optimised path (except last), adding the correct actions required to reach each next position
    prev_direction = Direction.NORTH
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

maze = create_maze(3, 3)
maze = add_vertical_wall(maze, 1, 2)
maze = add_vertical_wall(maze, 2, 2)
maze = add_horizontal_wall(maze, 1, 1)

runner = create_runner(0, 0, Direction.NORTH)

print(explore(runner, maze, (2,0)))

print(shortest_path(maze, (0,0), (2,0)))