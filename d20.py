from functools import cache
from typing import Any


from aocd import get_data
from util import Matrix, Index, add, print_path, sub

# Data
data = get_data(year=2024, day=20)

test = """\
###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############\
"""


# Convert data (text) to workable input
def parse(text: str) -> Matrix:
    return Matrix(text)


def path(matrix: Matrix) -> list[Index]:
    path = []
    for i in matrix.indices():
        if matrix.entry(i) == "S":
            path.append(i)
            break
    current_i = path[0]
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    for d in directions:
        next_i = add(current_i, d)
        if matrix.entry(next_i) == ".":
            path.append(next_i)
            current_i = next_i
            break
    while matrix.entry(current_i) != "E":
        for d in directions:
            next_i = add(current_i, d)
            if matrix.entry(next_i) != "#" and next_i != path[-2]:
                path.append(next_i)
                current_i = next_i
                break

    return path


# Part 1
ggwp = parse(test)
xd = path(ggwp)


# def can_jump(matrix: Matrix, i1: Index, i2: Index) -> bool:
#     (x1, y1), (x2, y2) = i1, i2
#     mid = ((x1 + x2) // 2, (y1 + y2) // 2)
#     return (
#         sub(i1, i2) in {(2, 0), (-2, 0), (0, 2), (0, -2)} and matrix.entry(mid) == "#"
#     )


# def save_count(matrix: Matrix, path: list[Index], pico: int, i: int) -> int:
#     # Idk why +2, but thats what gave the correct results on test-maze
#     return sum(1 for ind in path[i + pico + 2 :] if can_jump(matrix, path[i], ind))
#
#
# def total_save_count(matrix: Matrix, path: list[Index], pico: int) -> int:
#     count = 0
#     print()
#     for i in range(len(path)):
#         print(f"Checking jumps from {i}, current_count {count}\r", end="")
#         count += save_count(matrix, path, pico, i)
#     print()
#     return count
#     # return sum(save_count(matrix, path, pico, i) for i in range(len(path)))


def can_jump(
    matrix: Matrix, i1: Index, i2: Index, walls: frozenset[Index]
) -> bool:
    (x1, y1), (x2, y2) = i1, i2
    mid = ((x1 + x2) // 2, (y1 + y2) // 2)
    return sub(i1, i2) in {(2, 0), (-2, 0), (0, 2), (0, -2)} and mid in walls


def save_count(
    matrix: Matrix,
    path: list[Index],
    pico: int,
    i: int,
    walls: frozenset[Index],
) -> int:
    # Idk why +2, but thats what gave the correct results on test-maze
    current_ind = path[i]
    return sum(
        1
        for ind in path[i + pico + 2 :]
        if can_jump(matrix, current_ind, ind, walls)
    )


def total_save_count(matrix: Matrix, path: list[Index], pico: int) -> int:
    count = 0
    walls = frozenset(matrix.indices()) - frozenset(path)
    print()
    for i in range(len(path)):
        print(f"Checking jumps from {i}, current_count {count}\r", end="")
        count += save_count(matrix, path, pico, i, walls)
    print()
    return count
    # return sum(save_count(matrix, path, pico, i) for i in range(len(path)))


print(total_save_count(ggwp, xd, 100))


def part1(text: str, pico: int) -> int:
    matrix = parse(text)
    index_path = path(matrix)
    print(f"Path length:{len(index_path)}")
    return total_save_count(matrix, index_path, pico)


# print("Part 1 test:", part1(test, 0))
# print("Part 1 real:", part1(data, 100))

jump_20s = []
for i in range(-20, 21):
    k = 20 - abs(i)
    jump_20s.extend((i, j) for j in range(k, k + 1))
    # for j in range(-k, k + 1):
    #     jump_20s.append((i, j))


mid = {(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)}
new_jumps: list[Index] = [
    (x + 20, y + 20) for x, y in jump_20s if (x, y) not in mid
]
new_jumps2: set[Index] = set(new_jumps)
print(new_jumps)
t = "\n".join(["." * 100 for _ in range(100)])
t = Matrix(t)
print_path(t, new_jumps2)


def can_jumpv2(matrix: Matrix, i1: Index, i2: Index) -> bool:
    (x1, y1), (x2, y2) = i1, i2
    mid = ((x1 + x2) // 2, (y1 + y2) // 2)
    return (
        sub(i1, i2) in {(2, 0), (-2, 0), (0, 2), (0, -2)}
        and matrix.entry(mid) == "#"
    )


# Part 2


def part2(text: str) -> int:
    return 0


# print("Part 2 test:", part2(test))
# print("Part 2 real:", part2(data))
