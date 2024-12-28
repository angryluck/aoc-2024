from __future__ import annotations

from functools import cache
from itertools import chain, product

from aocd import get_data

from util import Matrix, add

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
type Code = str  # A string of buttons


# def is_straight(code: Code) -> bool:
#     has_changed = False
#     for a, b in zip(code[:-2], code[1:-1]):
#         if a != b:
#             if has_changed:
#                 return False
#             has_changed = True
#     return True
#
#
def filter_min(xs: list) -> list:
    return [x for x in xs if len(x) == min(len(y) for y in xs)]


# # For use in Keypad class
# def shortest_paths(indices: set[Index], start: Index, end: Index) -> list[Code]:
#     if start == end:
#         return ["A"]
#     ret = []
#     for d in DIRECTIONS:
#         if (step := add(start, d)) in indices:
#             ret.extend(
#                 DIRECTION_TO_CHAR[d] + code
#                 for code in shortest_paths(indices - {start}, step, end)
#             )
#             # for path in shortest_paths(indices - {start}, step, end):
#             #     ret.append([start] + path)
#     if not ret:
#         return []
#     ret = filter_min(ret)
#     return [x for x in ret if is_straight(x)]
#
#
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

        # self._shortest_paths = {
        #     (i1, i2): shortest_paths(self.indices, i1, i2)
        #     for i1, i2 in product(self.indices, self.indices)
        # }
        #

    def index(self, button: Button) -> Index:
        for index in self.indices:
            if self.matrix.entry(index) == button:
                return index
        raise KeyError(button)

    def val(self, index: Index) -> Button:
        if button := self.matrix.entry(index):
            return button
        raise KeyError(index)

    # def shortest_paths(
    #     self, start: Index | Button, end: Index | Button
    # ) -> list[Code]:
    #     if isinstance(start, str):
    #         start = self.index(start)
    #     if isinstance(end, str):
    #         end = self.index(end)
    #
    #     return self._shortest_paths[(start, end)]


numpad = Keypad("""\
789
456
123
.0A\
""")


dpad = Keypad("""\
.^A
<v>\
""")

# .^A
# <v>


# Psuedo: Rule: Always up-down first, then left-right.
# Don't focus on generalization -- focus on dpads. Example: we have that
# 029A is typed by <A ^A >^^A. So focus on this code!
# (v<<A ^>>A) (<A >A) ()
# (v<A) (<A) (A) (^>>A)


#
# v
# v<A
# v<<A >A >^A (irregular version)
# v<A <A >>^A
#
# cost("A->v", 25) =


# # @cache
# def type_code(keypad: Keypad, code: str) -> list[str]:
#     code = "A" + code
#     ret = []
#     for a, b in zip(code[:-1], code[1:]):
#         ret.append(keypad.shortest_paths(a, b))
#     combinations = list(product(*ret))
#     # reduce(...) is equivalent to sum(x, []), i.e. flattening of list
#     combinations_flat = ["".join(x) for x in combinations]
#     return filter_min(combinations_flat)
#
#
# # Convert data (text) to workable input
# def parse(text: str) -> list[str]:
#     return list(text.split("\n"))
#
#
# def part1(text: str) -> int:
#     code_list = parse(text)
#     retval = 0
#     for code in code_list:
#         print(f"Current code: {code}\r", end="")
#         val = int(code[:-1])
#         type_list = type_code(numpad, code)
#         type_list = filter_min(
#             list(chain.from_iterable(type_code(dpad, x) for x in type_list))
#         )
#         type_list = filter_min(
#             list(chain.from_iterable(type_code(dpad, x) for x in type_list))
#         )
#         # One more iterations, and this is too slow ;(
#         retval += len(type_list[0]) * val
#     print()
#
#     return retval
#
#
# # print(f"Part 1 test:\n{part1(test)}")
# # print(f"Part 1 real:\n{part1(data)}")
#
#
# def type_path(code: str) -> str:
#     return "".join(type_code(dpad, code))
#
#
# # Part 2
#
#
# def best_path(keypad: Keypad, start: Index, end: Index) -> Code:
#     cs = keypad.shortest_paths(start, end)
#     tmp = {}
#     for i in range(len(cs)):
#         c = cs[i]
#         xs = filter_min(type_code(dpad, c))
#         for _ in range(2):
#             xs = list(chain.from_iterable(type_code(dpad, x) for x in xs))
#             xs = filter_min(xs)
#         tmp[i] = len(xs[0])
#     best_i = min(tmp, key=lambda k: tmp[k])
#     return cs[best_i]
#
#
# BEST_NUMPAD_PATHS = {
#     (numpad.val(i1), numpad.val(i2)): best_path(numpad, i1, i2)
#     for i1, i2 in product(numpad.indices, numpad.indices)
# }
#
# BEST_DPAD_PATHS = {
#     (dpad.val(i1), dpad.val(i2)): best_path(dpad, i1, i2)
#     for i1, i2 in product(dpad.indices, dpad.indices)
# }
#
# # print(BEST_NUMPAD_PATHS)
# # print(BEST_DPAD_PATHS)
#
#
# def type_code_optim(paths: dict, code: str) -> str:
#     code = "A" + code
#     return "".join(paths[a, b] for a, b in zip(code[:-1], code[1:]))
#
#
# print("Starting optimization process:")
# c = type_code_optim(BEST_NUMPAD_PATHS, "029A")
# for i in range(2):
#     print(f"Iteration {i}\r", end="")
#     c = type_code_optim(BEST_DPAD_PATHS, c)
# print()
# print(len(c))
#
#
# def test_shortest_path(i: int) -> None:
#     cs = numpad.shortest_paths((1, 2), (2, 3))
#     c = cs[i]
#     cs = filter_min(type_code(dpad, c))
#     for _ in range(2):
#         cs = list(chain.from_iterable(type_code(dpad, x) for x in cs))
#         print([len(x) for x in cs])
#         cs = filter_min(cs)
#         print([len(x) for x in cs])
#     # Seems that distance is the same, from this point on.
#     ds = type_code(dpad, cs[-2])
#     print(len(ds), len(filter_min(ds)), len(ds[0]))
#     # for x in range(iterations):
#
#
# # for start, end in product(numpad.indices, numpad.indices):
# #     numpad._shortest_paths[start, end] = [best_path(numpad, start, end)]
#
# # print(numpad._shortest_paths)
#
# # print(best_path(numpad, (1, 2), (2, 3)))
# # for p in numpad.shortest_paths((1, 2), (2, 3)):
# #     c = "".join(p)
# #     p2 = type_code(dpad, c)
# #     print(p2)
# #     # for p3 in p2:
# #     #     c2 = "".join(p3)
# #     #     print([len(x) for x in type_code(dpad, c2)])
#
#
# def part2(text: str) -> int:
#     return 0
#
#
# # print(f"Part 2 test:\n{part2(test)}")
# # print(f"Part 2 real:\n{part2(data)}")
#
#
# # print(type_code(numpad, "029A"))
# # codes1 = type_code(numpad, "029A")
# # print([len(c) for c in codes1])
# # codes2 = list(chain.from_iterable(type_code(dpad, c) for c in codes1))
# # # codes2 = [type_code(dpad, c) for c in codes1]
# # codes2_min = [x for x in codes2 if len(x) == min(len(y) for y in codes2)]
# # # codes3 = list(chain.from_iterable(type_code(dpad, c) for c in codes2))
# # codes3 = type_code(dpad, codes2_min[0])
# # # print([len(c) for c in codes2])
# # codes3_min = [x for x in codes3 if len(x) == min(len(y) for y in codes3)]
# # # print(codes3_min)
# # # print([len(c) for c in codes3_min])
