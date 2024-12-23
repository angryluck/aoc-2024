from functools import cache, reduce
from typing import Any

from aocd import get_data

# Data
data = get_data(year=2024, day=22)

test = """\
1
10
100
2024\
"""


# Convert data (text) to workable input
def parse(text: str) -> list[int]:
    return [int(x) for x in text.split("\n")]


C = 16777216  # = 2**24, seems important, hmm
# As C is a power of 2, it distributes over XOR.
C2 = C - 1
# 64 == 2**6
# 32 == 2**5
# 2048 == 2**11


# Part 1
@cache
def mix_prune(num: int, secret_num: int) -> int:
    return (num ^ secret_num) % C


n = 809877309871294087


def step1(x: int) -> int:
    return ((x << 6) ^ x) & C2


def step2(x: int) -> int:
    return ((x >> 5) ^ x) & C2


def step3(x: int) -> int:
    return ((x << 11) ^ x) & C2


# def process(num: int) -> int:
#     return step3(step2(step1(num)))


def process(n: int) -> int:
    x1 = ((n << 6) ^ n) & C2
    x2 = ((x1 >> 5) ^ x1) & C2
    x3 = (x2 << 11 ^ x2) & C2
    # print(x3 % 10, end=" ")
    return x3
    # return (n << 12 ^ n << 6 ^ n << 17 ^ n << 11 ^ n << 1 ^ n >> 5 ^ n << 6 ^ n) & C2


# @cache
# def process(num: int) -> int:
#     num1 = mix_prune(num * 64, num)  # 64 == 2**6
#     num2 = mix_prune(num1 // 32, num1)  # 32 == 2**5
#     num3 = mix_prune(num2 * 2048, num2)  # 2048 == 2**11
#     # return num3 % C
#     n = num
#     return ((n * 64) ^ n) % C ^ (((n * 64) ^ n) % C)


@cache
def process_n_times(num: int, times: int) -> int:
    result = num
    for _ in range(times):
        result = process(result)
    return result


print(process_n_times(1, 2000))


def part1(text: str) -> int:
    nums = parse(text)
    return sum(process_n_times(x, 2000) for x in nums)


# if __name__ == "__main__":
#     print("Part 1 test:", part1(test))
#     print("Part 1 real:", part1(data))


# Part 2
test2 = """\
1
2
3
2024\
"""

type Sequence = tuple[int, int, int, int]
# Whenever a sequence seq shows up, add current bananana to seq_val[seq]
seq_val: dict[Sequence, int] = {}


def step(n: int) -> tuple[int, int]:
    """Return next secret number, and next number of bananas"""
    pre_val = n % 10
    next_val = process(n) % 10
    return next_val, (next_val - pre_val)


def banana_list(n: int) -> tuple[list[int], list[int]]:
    return ([], [])


# print(diff_val(15887950))

# def process(n: int) -> tuple[int, int]:
#     x1 = ((n << 6) ^ n) & C2
#     x2 = ((x1 >> 5) ^ x1) & C2
#     x3 = (x2 << 11 ^ x2) & C2
#     # print(x3 % 10, end=" ")
#     return x3, x3 % 10


def part2(text: str) -> int:
    return 0


# print("Part 2 test:", part2(test))
# print("Part 2 real:", part2(data))
