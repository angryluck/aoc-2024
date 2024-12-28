from functools import cache

from aocd import get_data

from util import Matrix

# Data
data = get_data(year=2024, day=21)

test = """\
029A
980A
179A
456A
379A\
"""


type Index = tuple[int, int]
type Button = str  # 0-9, >^<v or A
type Code = str  # A string of buttons


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

    def index(self, button: Button) -> Index:
        for index in self.indices:
            if self.matrix.entry(index) == button:
                return index
        raise KeyError(button)

    def val(self, index: Index) -> Button:
        if button := self.matrix.entry(index):
            return button
        raise KeyError(index)


NUMPAD = Keypad("""\
789
456
123
.0A\
""")


DPAD = Keypad("""\
.^A
<v>\
""")


def move_right(end: Index, start: Index, buf: Code) -> tuple[Index, Code]:
    (sx, sy), (ex, _) = start, end
    while sx < ex:
        buf += ">"
        sx += 1
    return (sx, sy), buf


def move_left(end: Index, start: Index, buf: Code) -> tuple[Index, Code]:
    (sx, sy), (ex, _) = start, end
    while sx > ex:
        buf += "<"
        sx -= 1
    return (sx, sy), buf


def move_up(end: Index, start: Index, buf: Code) -> tuple[Index, Code]:
    (sx, sy), (_, ey) = start, end
    while sy > ey:
        buf += "^"
        sy -= 1
    return (sx, sy), buf


def move_down(end: Index, start: Index, buf: Code) -> tuple[Index, Code]:
    (sx, sy), (_, ey) = start, end
    while sy < ey:
        buf += "v"
        sy += 1
    return (sx, sy), buf


def type_numpad_code(code: Code) -> list[Code]:
    """Only types numpad-codes."""
    code = "A" + code
    ret = []
    max_row = 3
    for a, b in zip(code[:-1], code[1:]):
        ret_code = ""
        start = NUMPAD.index(a)  # Start
        end = NUMPAD.index(b)  # End
        # Left column (1,4,7) to bottom row (0,A):
        if start[0] == 0 and end[1] == max_row:
            pos, ret_code = move_right(end, start, ret_code)
            _, ret_code = move_down(end, pos, ret_code)
        # Bottom row (0, A) to left column (1,,4,7):
        elif start[1] == max_row and end[0] == 0:
            pos, ret_code = move_up(end, start, ret_code)
            _, ret_code = move_left(end, start, ret_code)
        else:
            pos = start
            # This is optimal order (found by trial and error)
            for fun in move_left, move_down, move_up, move_right:
                pos, ret_code = fun(end, pos, ret_code)
        ret_code += "A"
        ret.append(ret_code)
    return ret


def type_code(code: Code) -> list[Code]:
    """Only types dpad-codes."""
    code = "A" + code
    ret = []
    for a, b in zip(code[:-1], code[1:]):
        ret_code = ""
        start = DPAD.index(a)  # Start
        end = DPAD.index(b)  # End
        # If start is "<", then go first right, then up
        if start == (0, 1):
            pos, ret_code = move_right(end, start, ret_code)
            _, ret_code = move_up(end, pos, ret_code)
        # If end is "<", then go first down, then left
        elif end == (0, 1):
            pos, ret_code = move_down(end, start, ret_code)
            _, ret_code = move_left(end, pos, ret_code)
        # Any other situation, we are in the 2x2 grid, so any order of
        # up/down/left/right works. The optimal way is to take those
        # buttons on the pad that are *furthest* away from A first.
        else:
            pos = start
            # up before right is optimal, not sure why
            for fun in move_left, move_down, move_up, move_right:
                pos, ret_code = fun(end, pos, ret_code)
        ret_code += "A"
        ret.append(ret_code)
    return ret


@cache
def shortest_length(robots: int, code: Code) -> int:
    if robots == 0:
        return len(code)
    return sum(shortest_length(robots - 1, x) for x in type_code(code))


def complexity(robots: int, code: Code) -> int:
    val = int(code[:-1])
    length = sum(shortest_length(robots - 1, x) for x in type_numpad_code(code))
    return length * val


def part1(text: str) -> int:
    codes = text.split("\n")
    return sum(complexity(3, x) for x in codes)


print("Part 1 test:", part1(test))
print("Part 1 real:", part1(data))


def part2(text: str) -> int:
    codes = text.split("\n")
    return sum(complexity(26, x) for x in codes)


print("Part 2 test:", part2(test))
print("Part 2 real:", part2(data))

# Values from other directions (top result didn't respect the no-go button)
# 194058481110036: Too low :(
# 492639922613608: Too high :(

# GRAVEYARD
#
#
# # Function meant to help find the optimal path, but found out by just trying
# # different things instead
# def possible_typed_codes(code: Code) -> list[set[Code]]:
#     """1 or 2 possible best codes, for each path."""
#     ret = []
#     code = "A" + code
#     for a, b in zip(code[:-1], code[1:]):
#         start, end = DPAD.index(a), DPAD.index(b)
#         if start == (0, 1):
#             ret.append({code_h_v(start, end)})
#             continue
#         if end == (0, 1):
#             ret.append({code_v_h(start, end)})
#             continue
#         ret.append({code_h_v(start, end), code_v_h(start, end)})
#     return ret
#
#
# def value(code) -> int:
#     return sum(len(s.pop()) for s in possible_typed_codes(code))
