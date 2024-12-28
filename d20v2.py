from aocd import get_data

from util import Index, Matrix, add

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


def distance(i1: Index, i2: Index) -> int:
    (x1, y1), (x2, y2) = i1, i2
    return abs(x1 - x2) + abs(y1 - y2)


def save_count_exact(path: list[Index], picoseconds: int) -> int:
    count = 0
    for i in range(len(path)):
        start = path[i]
        for j in range(i + picoseconds, len(path)):
            diff = j - i
            end = path[j]
            dist = distance(start, end)
            if diff - dist == picoseconds and dist <= 20:  # noqa: PLR2004
                count += 1
    return count


def save_count_at_least(path: list[Index], picoseconds: int) -> int:
    count = 0
    print("Length:", len(path))
    for i in range(len(path)):
        print(f"Current index: {i}\r", end="")
        start = path[i]
        for j in range(i + picoseconds, len(path)):
            diff = j - i
            end = path[j]
            dist = distance(start, end)
            # Max 20 picosecond jump!
            if diff - dist >= picoseconds and dist <= 20:  # noqa: PLR2004
                count += 1
    print()
    return count


def part2(text: str) -> int:
    p = path(parse(text))
    # for i in range(len(p)):
    #     saved = save_count_exact(p, i)
    #     if saved != 0:
    #         print(f"{save_count_exact(p, i)} cheats save {i} picoseconds")
    return save_count_at_least(p, 100)


print("Part 2 test:", part2(test))
print("Part 2 real:", part2(data))
