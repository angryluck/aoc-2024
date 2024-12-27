from __future__ import annotations
from functools import cache, reduce
from itertools import chain, product
from typing import Any

from aocd import get_data
from util import Matrix, add

from itertools import product
import operator

# Data
data = get_data(year=2024, day=21)

test = """\
029A
980A
179A
456A
379A\
"""


DIRECTIONS = {(0, -1), (-1, 0), (1, 0), (0, 1)}
CHAR_TO_DIRECTION = {"^": (0, -1), "<": (-1, 0), ">": (1, 0), "v": (0, 1)}
DIRECTION_TO_CHAR = {(0, -1): "^", (-1, 0): "<", (1, 0): ">", (0, 1): "v"}

type Direction = tuple[int, int]
type Index = tuple[int, int]
type Button = str  # 0-9, >^<v or A


def is_straight(path: list[Button]) -> bool:
    has_changed = False
    for a, b in zip(path[:-2], path[1:-1]):
        if a != b:
            if has_changed:
                return False
            has_changed = True
    return True


def filter_min(xs: list) -> list:
    return [x for x in xs if len(x) == min(len(y) for y in xs)]


# For use in Keypad class
def shortest_paths(
    indices: set[Index], start: Index, end: Index
) -> list[list[Button]]:
    if start == end:
        return [["A"]]
    ret = []
    for d in DIRECTIONS:
        if (step := add(start, d)) in indices:
            ret.extend(
                [DIRECTION_TO_CHAR[d], *path]
                for path in shortest_paths(indices - {start}, step, end)
            )
            # for path in shortest_paths(indices - {start}, step, end):
            #     ret.append([start] + path)
    if not ret:
        return []
    ret = filter_min(ret)
    return [x for x in ret if is_straight(x)]


class Keypad:
    """Functions and data needed for any keypad."""

    def __init__(self, text: str):
        self.matrix = Matrix(text)
        self.indices = {
            i for i in self.matrix.indices() if self.matrix.entry(i) != "."
        }
        self._index_to_val = {
            index: val
            for index in self.indices
            if (val := self.matrix.entry(index))  # To avoid lint error
        }
        self._val_to_index = {
            self.matrix.entry(index): index for index in self.indices
        }
        self._shortest_paths = {
            (i1, i2): shortest_paths(self.indices, i1, i2)
            for i1, i2 in product(self.indices, self.indices)
        }

    def index(self, button: Button) -> Index:
        for index in self.indices:
            if self.matrix.entry(index) == button:
                return index
        raise KeyError(button)

    def val(self, index: Index) -> Button:
        if button := self.matrix.entry(index):
            return button
        raise KeyError(index)

    def shortest_paths(
        self, start: Index | Button, end: Index | Button
    ) -> list[list[Button]]:
        if isinstance(start, str):
            start = self.index(start)
        if isinstance(end, str):
            end = self.index(end)

        return self._shortest_paths[(start, end)]


numpad = Keypad("""\
789
456
123
.0A\
""")


# for l in numpad.shortest_paths("7", "3"):
# print(l)
# print(is_straight(l))


dpad = Keypad("""\
.^A
<v>\
""")


@cache
def type_code(keypad: Keypad, code: str) -> list[str]:
    code = "A" + code
    ret = []
    for a, b in zip(code[:-1], code[1:]):
        ret.append(keypad.shortest_paths(a, b))
    combinations = list(product(*ret))
    # reduce(...) is equivalent to sum(x, []), i.e. flattening of list
    combinations_flat = ["".join(chain.from_iterable(x)) for x in combinations]
    return filter_min(combinations_flat)


# print(type_code(numpad, "029A"))
# codes1 = type_code(numpad, "029A")
# print([len(c) for c in codes1])
# codes2 = list(chain.from_iterable(type_code(dpad, c) for c in codes1))
# # codes2 = [type_code(dpad, c) for c in codes1]
# codes2_min = [x for x in codes2 if len(x) == min(len(y) for y in codes2)]
# # codes3 = list(chain.from_iterable(type_code(dpad, c) for c in codes2))
# codes3 = type_code(dpad, codes2_min[0])
# # print([len(c) for c in codes2])
# codes3_min = [x for x in codes3 if len(x) == min(len(y) for y in codes3)]
# # print(codes3_min)
# # print([len(c) for c in codes3_min])


# print(numpad.shortest_paths("A", "0"))
# print(numpad.shortest_paths("0", "2"))
# print(numpad.shortest_paths("2", "9"))
# print(numpad.shortest_paths("9", "A"))


# Convert data (text) to workable input
def parse(text: str) -> list[str]:
    return list(text.split("\n"))


# print(parse(test))
# print(parse(data))


def part1(text: str) -> int:
    code_list = parse(text)
    retval = 0
    # numpad = Keypad("""\
    # 789
    # 456
    # 123
    # .0A\
    # """)
    # dpad = Keypad("""\
    # .^A
    # <v>\
    # """)
    for code in code_list:
        print(f"Current code: {code}\r", end="")
        val = int(code[:-1])
        type_list = type_code(numpad, code)
        type_list = filter_min(
            list(chain.from_iterable(type_code(dpad, x) for x in type_list))
        )
        type_list = filter_min(
            list(chain.from_iterable(type_code(dpad, x) for x in type_list))
        )
        # One more iterations, and this is too slow ;(
        retval += len(type_list[0]) * val
    print()

    return retval


print(f"Part 1 test:\n{part1(test)}")
print(f"Part 1 real:\n{part1(data)}")


# Part 2


def part2(text: str) -> int:
    return 0


# print(f"Part 2 test:\n{part2(test)}")
# print(f"Part 2 real:\n{part2(data)}")
