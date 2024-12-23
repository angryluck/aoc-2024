from aocd import get_data
from numpy._typing import NDArray
import pyparsing
from pyparsing import Char, Suppress, Literal
import numpy as np

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
    xy = val + Suppress(",") + val
    button_line = button + xy
    prize_line = prize + xy
    parse_block = button_line + button_line + prize_line
    blocks = text.split("\n\n")
    res = []
    for block in blocks:
        nums = parse_block.parseString(block)
        matrix = np.array(nums[:4]).reshape(2, 2).T
        prize = np.array(nums[4:]).reshape(2, 1)
        res.append((matrix, prize))
    return res


gg = parse(test)
# tm, tx = gg[1]
# print(tm, tx)
# print(np.linalg.inv(tm))


def tokens(block):
    tm, tx = block
    vals = np.linalg.inv(tm) @ tx
    if all(np.allclose(x, np.round(x)) for x in vals):
        token_price = np.array([3, 1]).reshape(2, 1)
        return round((vals.T @ token_price).item())
    return 0


G = 10000000000000

# First array: 2x2 matrix of cost pr. button
# Second array: 2-vector of end-prize
type Block = tuple[NDArray, NDArray]


def part1(text: str) -> int:
    blocks = parse(text)
    return sum(tokens(x) for x in blocks)


# print("Part 1 test:", part1(test))
# print("Part 1 real:", part1(data))


# Part 2
def parse2(text: str) -> list[tuple[NDArray, NDArray]]:
    button = Suppress(Literal("Button") + Char("AB") + Literal(":"))
    prize = Suppress(Literal("Prize:"))
    val = Suppress(Char("XY") + Char("+=")) + pyparsing.common.integer
    xy = val + Suppress(",") + val
    button_line = button + xy
    prize_line = prize + xy
    parse_block = button_line + button_line + prize_line
    blocks = text.split("\n\n")
    res = []
    for block in blocks:
        nums = parse_block.parseString(block)
        matrix = np.array(nums[:4], dtype=np.float64).reshape(2, 2).T
        prize = np.array(nums[4:], dtype=np.float64).reshape(2, 1)
        prize += 10000000000000
        res.append((matrix, prize))
    return res


def tokens2(block):
    tm, tx = block
    vals = np.linalg.inv(tm) @ tx
    fracs = np.modf(vals)[0]
    if all(np.isclose(x, 0, 0.01, 0.01) or np.isclose(x, 1, 0.01, 0.01) for x in fracs):
        token_price = np.array([3, 1]).reshape(2, 1)
        ret = (vals.T @ token_price).item()
        return round(ret)
    return 0


def part2(text: str) -> int:
    blocks = parse2(text)
    # for x in blocks:
    # print(tokens2(x))
    return sum(tokens2(x) for x in blocks)
    # return sum(tokens(x) for x in blocks)


print("Part 2 test:", part2(test))
print("Part 2 real:", part2(data))
