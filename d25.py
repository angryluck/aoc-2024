from typing import Any

import numpy as np
from aocd import get_data

# Data
data = get_data(year=2024, day=25)

test = """\
#####
.####
.####
.####
.#.#.
.#...
.....

#####
##.##
.#.##
...##
...#.
...#.
.....

.....
#....
#....
#...#
#.#.#
#.###
#####

.....
.....
#.#..
###..
###.#
###.#
#####

.....
.....
.....
#....
#.#..
#.#.#
#####\
"""


# Convert data (text) to workable input
def parse(text: str) -> Any:
    blocks = text.split("\n\n")
    locks = [b for b in blocks if b[0] == "#"]
    keys = [b for b in blocks if b[0] == "."]
    locks = np.array(
        [
            [sum(c[i] == "#" for c in b.split("\n")) - 1 for i in range(5)]
            for b in locks
        ]
    )
    keys = np.array(
        [
            [sum(c[i] == "#" for c in b.split("\n")) - 1 for i in range(5)]
            for b in keys
        ]
    )
    return locks, keys


# print(parse(test))
# print(parse(data))
# Part 1


def part1(text: str) -> int:
    locks, keys = parse(text)
    combinations = np.add(
        locks[:, np.newaxis], keys
    )  # Adds each row of locks to each
    combinations = np.reshape(combinations, (-1, combinations.shape[-1]))
    return np.sum(~np.any(combinations >= 6, axis=1))
    # row of keys
    # return 0


print(f"Part 1 test:\n{part1(test)}")
print(f"Part 1 real:\n{part1(data)}")


# Part 2


def part2(text: str) -> int:
    return 0


# print(f"Part 2 test:\n{part2(test)}")
# print(f"Part 2 real:\n{part2(data)}")
