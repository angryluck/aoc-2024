"""Solution to day16 of Advent of Code, 2024."""

from __future__ import annotations

import operator
import timeit
from functools import reduce

from aocd import get_data, sys

from util import Matrix, add

type Index = tuple[int, int]
# Data
data = get_data(year=2024, day=16)

test = """\
###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############"""

test2 = """\
#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
################# """


# Convert data (text) to workable input
def parse(text: str) -> tuple[Matrix, Index, Index]:
    maze = Matrix(text)
    start = (-1, -1)
    end = (-1, -1)
    for index in maze.indices:
        if maze.entry(index) == "S":
            start = index
        if maze.entry(index) == "E":
            end = index
    if start == (-1, -1) or end == (-1, -1):
        msg = "Start 'S' or end 'E' not found in maze"
        raise ValueError(msg)
    return Matrix(text), start, end


# Part 1
def rotate_left(index: Index) -> Index:
    (i, j) = index
    return (j, -i)


def rotate_right(index: Index) -> Index:
    (i, j) = index
    return (-j, i)


def path_1(maze: Matrix, start: Index) -> dict[Index, int]:
    """Compute shortest path using disjktra's algorithm."""
    # Naive recursion was too slow
    unvisited: set[Index] = {i for i in maze.indices if maze.entry(i) != "#"}
    min_cost: dict[Index, int] = {i: sys.maxsize for i in unvisited}
    best_direction: dict[Index, Index] = {start: (1, 0)}
    min_cost[start] = 0

    def update_cost(i: Index, direction: Index, new_cost: int) -> None:
        pre_cost = min_cost[i]
        if new_cost < pre_cost:
            min_cost[i] = new_cost
            best_direction[i] = direction

    while unvisited:  # Checks if unvisited is non-empty
        current_index = min(unvisited, key=lambda x: min_cost[x])
        current_cost = min_cost[current_index]
        current_direction = best_direction[current_index]
        update_cost(current_index, current_direction, current_cost + 1)
        for d, c in (
            (current_direction, 1),
            (rotate_right(current_direction), 1001),
            (rotate_left(current_direction), 1001),
        ):
            new_index = add(current_index, d)
            if new_index in unvisited:
                update_cost(add(current_index, d), d, current_cost + c)
        unvisited.remove(current_index)
    return min_cost


def part1(text: str) -> int:
    maze, start, end = parse(text)
    costs = path_1(maze, start)

    return costs[end]


print("Part 1 test:", part1(test))
print("Part 1 test 2:", part1(test2))
start = timeit.default_timer()
result = part1(data)
time_taken = timeit.default_timer() - start
print(f"Part 1 real ({time_taken:.2f} seconds):", result)

# Direction is one of the 4 indices (1,0), (-1,0), (0,1) and (0,-1)
type Direction = tuple[int, int]
type Step = tuple[Index, Direction]


# Part 2
def path_2(
    maze: Matrix, start: Index
) -> tuple[dict[Step, set[Index]], dict[Step, int]]:
    """Compute shortest path using distra's algorithm."""
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    # Unvisited: set tuples of position, and direction when entering
    unvisited: set[Step] = {
        (i, d) for i in maze.indices if maze.entry(i) != "#" for d in directions
    }
    min_cost: dict[Step, int] = {p: sys.maxsize for p in unvisited}
    best_path: dict[Step, set[Index]] = {(start, (1, 0)): {start}}
    min_cost[(start, (1, 0))] = 0

    def next_steps(s: Step) -> list[tuple[Step, int]]:
        i, d = s
        d_r = rotate_right(d)
        d_l = rotate_left(d)
        potential_steps = [
            ((add(i, d), d), 1),
            ((add(i, d_r), d_r), 1001),
            ((add(i, d_l), d_l), 1001),
        ]
        return [(s, c) for (s, c) in potential_steps if s in unvisited]

    def update_cost(s_now: Step, s_prev: Step, new_cost: int) -> None:
        # Now i is previous index, so we can compare
        # prev_i = sub(i, direction)
        pre_cost = min_cost[s_now]
        if new_cost == pre_cost:
            # s_now[0] is already in best_path[s_now], but adding to be safe
            best_path[s_now] = best_path[s_now] | best_path[s_prev] | {s_now[0]}
        if new_cost < pre_cost:
            min_cost[s_now] = new_cost
            best_path[s_now] = best_path[s_prev] | {s_now[0]}

    while unvisited:  # Checks if unvisited is non-empty
        current_step = min(unvisited, key=lambda x: min_cost[x])
        current_cost = min_cost[current_step]
        for s, c in next_steps(current_step):
            update_cost(s, current_step, current_cost + c)
        unvisited.remove(current_step)
        print(f"Removed step {current_step}  \r", end="")
    print("DONE", " " * 40)
    return best_path, min_cost


def path_3(
    maze: Matrix, start: Index
) -> tuple[dict[Step, set[Index]], dict[Step, int]]:
    # An attempt at optimizing path_2, by reducing the amount of indices we have
    # to compute 'min' of.
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    # Add as needed instead"
    unvisited: set[Step] = {
        (i, d) for i in maze.indices if maze.entry(i) != "#" for d in directions
    }
    min_cost: dict[Step, int] = {(start, (1, 0)): 0}
    best_path: dict[Step, set[Index]] = {(start, (1, 0)): {start}}

    def next_steps(s: Step) -> list[tuple[Step, int]]:
        i, d = s
        d_r = rotate_right(d)
        d_l = rotate_left(d)
        potential_steps = [
            ((add(i, d), d), 1),
            ((add(i, d_r), d_r), 1001),
            ((add(i, d_l), d_l), 1001),
        ]
        return [
            (s, c)
            for (s, c) in potential_steps
            if (val := maze.entry(s[0])) and val in ".E"
        ]

    def update_cost(s_now: Step, s_prev: Step, new_cost: int) -> None:
        # Now i is previous index, so we can compare
        pre_cost = min_cost.setdefault(s_now, sys.maxsize)
        if new_cost == pre_cost:
            best_path[s_now] = best_path[s_now] | best_path[s_prev] | {s_now[0]}
        if new_cost < pre_cost:
            min_cost[s_now] = new_cost
            best_path[s_now] = best_path[s_prev] | {s_now[0]}

    # Check if any indices left in intersection of unvisited and min_cost
    while to_check := unvisited & min_cost.keys():
        current_step = min(to_check, key=lambda x: min_cost[x])
        current_cost = min_cost[current_step]
        for s, c in next_steps(current_step):
            update_cost(s, current_step, current_cost + c)
        unvisited.remove(current_step)
    return best_path, min_cost


def print_path(maze: Matrix, indices: set[Index]) -> None:
    for j in range(maze.rows):
        for i in range(maze.cols):
            if (i, j) in indices:
                print("O", end="")
            else:
                print(maze.entry_ij(i, j), end="")
        print()


def part2(text: str) -> int:
    maze, start, end = parse(text)
    paths, costs = path_2(maze, start)
    # print(paths)
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    best_cost = min([costs[(end, d)] for d in directions])
    best_paths = [
        paths[(end, d)] for d in directions if costs[(end, d)] == best_cost
    ]
    combined_path = reduce(operator.or_, best_paths)

    return len(combined_path)


def part2_v2(text: str) -> int:
    maze, start, end = parse(text)
    paths, costs = path_3(maze, start)
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    best_cost = min([costs.get((end, d), sys.maxsize) for d in directions])
    best_paths = [
        paths.get((end, d), set())
        for d in directions
        if costs.get((end, d), sys.maxsize) == best_cost
    ]
    combined_path = reduce(operator.or_, best_paths)

    return len(combined_path)


print("Part 2 test:", part2_v2(test))
print("Part 2 test 2:", part2_v2(test2))
start = timeit.default_timer()
result = part2_v2(data)
time_taken = timeit.default_timer() - start
time_taken = timeit.timeit(lambda: part2_v2(data), number=1)
print(f"Part 2 real ({time_taken:.2f} seconds):", result)
