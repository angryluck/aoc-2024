from itertools import product

from aocd import get_data

from util import Index, Matrix

from functools import partial

# Data
data = get_data(year=2024, day=10)

test = """\
89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732"""


# Convert data (text) to workable input
def parse(text: str) -> Matrix:
    return Matrix(text, (lambda x: -1 if x == "." else int(x)))


gg = parse(test)
# print(gg.matrix)
# print(gg.entry(0,0))
# print(gg.move(0,1,0,0))


def valid_steps(topo: Matrix, current_index: Index) -> list[Index]:
    current_val = topo.entry(current_index)
    if current_val is None:
        return []

    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    return [
        res[0]
        for d in directions
        if (res := topo.move(current_index, d)) and res[1] == current_val + 1
    ]


MAX_VAL = 9


def recursive_steps(topo: Matrix, current_index: Index) -> set[Index]:
    if topo.entry(current_index) == MAX_VAL:
        return {current_index}
    next_steps = set()
    for step in valid_steps(topo, current_index):
        next_steps.update(recursive_steps(topo, step))
    return next_steps


# Part 1


def part1(text: str) -> int:
    topo = parse(text)
    return sum(
        len(recursive_steps(topo, (i, j)))
        for i, j in product(range(topo.cols), range(topo.rows))
        if topo.entry((i, j)) == 0
    )


print("Part 1 test:", part1(test))
print("Part 1 real:", part1(data))


# Part 2

test2 = """\
.....0.
..4321.
..5..2.
..6543.
..7..4.
..8765.
..9...."""


def recursive_steps_list(topo: Matrix, current_index: Index) -> list[Index]:
    if topo.entry(current_index) == MAX_VAL:
        return [current_index]
    next_steps = []
    for step in valid_steps(topo, current_index):
        next_steps.extend(recursive_steps_list(topo, step))
    return next_steps


def part2(text: str) -> int:
    topo = parse(text)
    # for i,j in product(range(topo.cols), range(topo.rows)):
    # if topo.entry((i,j))==0:
    # print("Index: ", (i,j))
    # print(recursive_steps_list(topo, (i,j)))
    return sum(
        len(recursive_steps_list(topo, (i, j)))
        for i, j in product(range(topo.cols), range(topo.rows))
        if topo.entry((i, j)) == 0
    )


print("Part 2 test:", part2(test2))
print("Part 2 test:", part2(test))
print("Part 2 real:", part2(data))
