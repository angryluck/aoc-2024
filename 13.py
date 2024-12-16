from aocd import get_data
import pyparsing
from pyparsing import Char, DelimitedList, Suppress, Literal

# Data
data = get_data(year=2024, day=13)

test = """\
Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279"""


# Convert data (text) to workable input
def parse(text: str):
    button = Suppress(Literal("Button") + Char("AB") + Literal(":"))
    prize = Suppress(Literal("Prize:"))
    val = Suppress(Char("XY") + Char("+=")) + pyparsing.common.integer
    xy = DelimitedList(val)
    button_line = button + xy
    prize_line = prize + xy
    block = button_line + button_line + prize_line
    lines = text.split("\n\n")
    return [block.parseString(line) for line in lines]


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
