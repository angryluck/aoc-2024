from typing import Any
import sys
from util import Matrix, add, print_path

from typing import cast

from aocd import get_data
import pyparsing as pp

# Data
data = get_data(year=2024, day=18)

test = """\
5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0\
"""

parse_index = pp.common.number + pp.Suppress(",") + pp.common.number
parse_index.set_parse_action(lambda t: (t[0], t[1]))

type Index = tuple[int, int]


# Convert data (text) to workable input
def parse(text: str, grid_size: int, byte_count: int) -> Matrix:
    matrix = "\n".join(["." * grid_size] * grid_size)
    matrix = Matrix(matrix)
    text_split = text.split("\n")
    for i in range(byte_count):
        index: Index = cast(Index, parse_index.parse_string(text_split[i])[0])
        matrix.set(index, "#")
    return matrix


# Part 1


def path(maze: Matrix) -> tuple[set[Index], int]:
    start = (0, 0)
    end = (maze.cols - 1, maze.rows - 1)
    # Input: maze, start_index, and end_index, Output: (one of) the shortest
    # path(s) from start to end.
    # Copied and modified from path_3 from d16.py
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    # Add as needed instead"
    unvisited: set[Index] = {i for i in maze.indices() if maze.entry(i) != "#"}
    min_cost: dict[Index, int] = {start: 0}
    best_path: dict[Index, set[Index]] = {start: {start}}

    def update_cost(prev_index: Index, new_index: Index, new_cost: int) -> None:
        # Now i is previous index, so we can compare
        pre_cost = min_cost.setdefault(new_index, sys.maxsize)
        # if new_cost == pre_cost:
        #     best_path[s_now] = best_path[s_now] | best_path[s_prev] | {s_now[0]}
        if new_cost < pre_cost:
            min_cost[new_index] = new_cost
            best_path[new_index] = best_path[prev_index] | {new_index}

    # Check if any indices left in intersection of unvisited and min_cost
    while to_check := unvisited & min_cost.keys():
        current_index = min(to_check, key=lambda x: min_cost[x])
        current_cost = min_cost[current_index]
        for i in unvisited & {add(current_index, d) for d in directions}:
            update_cost(current_index, i, current_cost + 1)
        unvisited.remove(current_index)
    return best_path.get(end, set()), min_cost.get(end, -1)


# gg = parse(test, 7, 12)
# print(gg)
#
#
# ggwp = parse(data, 71, 1024)
#
# path_test = path(gg)
# print_path(gg, path_test)
# path_test = path(ggwp)
# print_path(ggwp, path_test)


def part1(text: str, grid_size: int, byte_count: int) -> int:
    print(len(text.split("\n")))
    print(text.split("\n")[3036])
    maze = parse(text, grid_size, byte_count)
    best_path, steps = path(maze)
    print_path(maze, best_path)
    return steps


# print("Part 1 test:", part1(test, 7, 12))
# print("Part 1 real:", part1(data, 71, 1024))


# Part 2
# Part 2 can pretty easily just be solved by trial and error, but we will try to
# automate


def part2(text: str, grid_size: int, start_byte_count: int) -> tuple[int, int]:
    maze = parse(text, grid_size, start_byte_count)
    # to_tuple = tuple(map(int, t.split(",")))
    byte_coordinates = [
        (int(tt[0]), int(tt[1]))
        for t in text.split("\n")
        if (tt := t.split(","))
    ]
    cast(list[Index], byte_coordinates)
    print(byte_coordinates)
    best_path, cost = path(maze)
    print(best_path)
    c = start_byte_count
    b = byte_coordinates[c]
    while cost != -1:
        b = byte_coordinates[c]
        print(maze, best_path)
        maze.set(b, "#")
        if b in best_path:
            print(maze)
            best_path, cost = path(maze)
            print("WHOHO", best_path)
        c += 1
        # if cost == -1:
        #     return b
    return b


print("Part 2 test:", part2(test, 7, 12))
# print("Part 2 real:", part2(data))
