from collections import Counter
from functools import partial, reduce
from itertools import count
from time import sleep
from typing import Any, Callable
import pyparsing as pp
from aocd import get_data
from math import prod
from util import Matrix, print_path

# Data
data = get_data(year=2024, day=14)

test = """\
p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3\
"""

type Position = tuple[int, int]
type Velocity = tuple[int, int]
type Robot = tuple[Position, Velocity]


# Convert data (text) to workable input
def parse(text: str) -> list[Robot]:
    coord = pp.common.number + pp.Suppress(",") + pp.common.number
    coord.set_parse_action(lambda t: (t[0], t[1]))
    p_parse = pp.Suppress("p=") + coord
    v_parse = pp.Suppress("v=") + coord
    total = p_parse + v_parse
    return [tuple(list(total.parse_string(x))) for x in text.split("\n")]


def move(x_size: int, y_size: int, robot: Robot) -> Robot:
    (x, y), (vx, vy) = robot
    new_x = (x + vx) % x_size
    new_y = (y + vy) % y_size
    return ((new_x, new_y), (vx, vy))


def one_second(move: Callable[[Robot], Robot], robots: list[Robot]) -> list[Robot]:
    return [move(x) for x in robots]


def simulate(
    seconds: int, mover: Callable[[Robot], Robot], robots: list[Robot]
) -> list[Robot]:
    return reduce(lambda x, _: one_second(mover, x), range(seconds), robots)


def safety(x_size: int, y_size: int, robots: list[Robot]) -> int:
    mx = x_size // 2
    my = y_size // 2
    robot_poss = [x[0] for x in robots]
    tl = [(x, y) for (x, y) in robot_poss if x < mx and y < my]
    tr = [(x, y) for (x, y) in robot_poss if x > mx and y < my]
    bl = [(x, y) for (x, y) in robot_poss if x < mx and y > my]
    br = [(x, y) for (x, y) in robot_poss if x > mx and y > my]
    return prod(len(x) for x in (tl, tr, bl, br))


# part 1


def part1(text: str, x_size: int, y_size: int) -> int:
    robots = parse(text)
    mover = partial(move, x_size, y_size)
    robots = simulate(100, mover, robots)
    return safety(x_size, y_size, robots)


print("Part 1 test:", part1(test, 7, 11))
print("Part 1 real:", part1(data, 101, 103))


# Part 2
def easter_egg(x_size: int, y_size: int, robots: list[Robot]) -> int:
    matrix = Matrix("\n".join([" " * x_size] * y_size))
    mover = partial(move, x_size, y_size)
    # max_y = y_size - 15
    # max_x = x_size - 15
    # Looking at pictures, often some vertical lines show up, and some
    # horizontal.
    # Vertical: 23 - 53 (+1 in vim, but these are python indices)
    # Horizontal: 25-57
    min_k = -1
    robot_counts: dict[Position, int] = {}
    with open("robot-tree.txt", "w") as f:
        print("", end="", file=f)
    with open("robot-tree.txt", "a") as f:
        # K: 3145
        # for i in range(1, 4390 * 2):
        # for k in range(1, 4390):
        for k in range(1, 100000):
            print(f"Checking iteration k = {k}\r", end="")
            robots = one_second(mover, robots)
            h_count = sum(1 for ((x, y), (_, _)) in robots if x == 23 or x == 53)
            v_count = sum(1 for ((x, y), (_, _)) in robots if y == 26 or y == 58)
            if v_count > 60 and h_count > 60:
                print()
                print(
                    "We have found a frame with dimensions",
                    v_count,
                    h_count,
                    f"at k={k}, see 'robot-tree.txt' for picture.",
                )
                if min_k == -1:
                    min_k = k
                robot_inds = [x for (x, _) in robots]
                # if any(
                #     x + y < 15 or x + y > x_size + y_size - 15 for (x, y) in robot_inds
                # ):
                # continue
                robot_counts = dict(Counter(robot_inds))

                for j in range(matrix.rows):
                    for i in range(matrix.cols):
                        if (i, j) in robot_counts:
                            print(str(robot_counts[(i, j)]), end="", file=f)
                        else:
                            print(" ", end="", file=f)
                    print(file=f)
                    # robot_inds = list(x for (x, _) in robots)
                # if all(x > 20 or y < max_y for (x, y) in robot_inds):
                # print_path(matrix, robot_inds, char="█", file=f)
                print("=" * x_size, "k=", k, file=f)
            # return k
        print("vim: nowrap", file=f)
    print()
    return min_k


def part2(text: str, x_size: int, y_size: int) -> int:
    robots = parse(text)
    return easter_egg(x_size, y_size, robots)


# print("Part 2 test:", part2(test))
print("Part 2 real:", part2(data, 101, 103))
