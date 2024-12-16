# from typing import Any
from __future__ import annotations

from aocd import get_data

from util import Matrix, add

# from itertools import product


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
def parse(text: str) -> tuple[Index, Index, Matrix]:
    maze = Matrix(text)
    start = (-1, -1)
    end = (-1, -1)
    for index in maze.indices:
        if maze.entry(index) == "S":
            start = index
        if maze.entry(index) == "E":
            end = index
    return start, end, Matrix(text)


print(parse(test))
print(parse(test2))
(start, end, gg) = parse(test)
print(gg)


def step(
    maze: Matrix, pos: Index, direction: Index, visited: set[Index]
) -> Index | None:
    new_index = add(pos, direction)
    if new_index in visited:
        return None
    if (val := maze.entry(new_index)) and val != "#":
        return new_index
    return None


# Part 1


def part1(text: str) -> int:
    return 0


# print("Part 1 test:", part1(test))
# print("Part 1 real:", part1(data))


# Part 2


def part2(text: str) -> int:
    return 0


# print("Part 2 test:", part2(test))
# print("Part 2 real:", part2(data))
