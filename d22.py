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
def mix_prune(num: int, secret_num: int) -> int:
    return (num ^ secret_num) % C


def process(n: int) -> int:
    tmp1 = ((n << 6) ^ n) & C2
    tmp2 = ((tmp1 >> 5) ^ tmp1) & C2
    return (tmp2 << 11 ^ tmp2) & C2


def process_n_times(num: int, times: int) -> int:
    result = num
    for _ in range(times):
        result = process(result)
    return result


# @cache
# def process_n_times(num: int, times: int) -> int:
#     if times == 0:
#         return num
#     return process_n_times(process(num), times - 1)


def part1(text: str) -> int:
    nums = parse(text)
    return sum(process_n_times(x, 2000) for x in nums)


if __name__ == "__main__":
    print("Part 1 test:", part1(test))
    print("Part 1 real:", part1(data))


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


def step(n: int) -> tuple[int, int, int]:
    """Return next secret number, and next number of bananas."""
    pre_val = n % 10
    next_val = process(n) % 10
    return secret, next_val, (next_val - pre_val)


def banana_list(n: int) -> tuple[list[int], list[int]]:
    return ([], [])


def diff_dict(times: int, secret: int) -> dict[Sequence, int]:
    """Return how my banans each sequence would give."""
    ret_dict = {}
    x0 = secret % 10
    tmp = process(secret)
    x1 = tmp % 10
    tmp = process(tmp)
    x2 = tmp % 10
    tmp = process(tmp)
    x3 = tmp % 10
    tmp = process(tmp)
    x4 = tmp % 10
    diff = (x1 - x0, x2 - x1, x3 - x2, x4 - x3)
    ret_dict.setdefault(diff, x4)
    for _ in range(4, times):
        x0 = x1
        x1 = x2
        x2 = x3
        x3 = x4
        tmp = process(tmp)
        x4 = tmp % 10
        diff = (x1 - x0, x2 - x1, x3 - x2, x4 - x3)
        ret_dict.setdefault(diff, x4)

    return ret_dict


# d1 = diff_dict(2000, 1)
# d2 = diff_dict(2000, 2)
# d3 = diff_dict(2000, 3)
# d4 = diff_dict(2000, 2024)
#
# # print(d1[(5, -1, -5, 6)])
# # print(d2[(5, -1, -5, 6)])
# # print(d3[(5, -1, -5, 6)])
# # print(d4[(5, -1, -5, 6)])
#
# d = reduce(
#     lambda x, y: {k: x.get(k, 0) + y.get(k, 0) for k in x.keys() | y.keys()},
#     [d1, d2, d3, d4],
# )
#
# print(max(d, key=d.get))
# print(diff_val(15887950))

# def process(n: int) -> tuple[int, int]:
#     x1 = ((n << 6) ^ n) & C2
#     x2 = ((x1 >> 5) ^ x1) & C2
#     x3 = (x2 << 11 ^ x2) & C2
#     # print(x3 % 10, end=" ")
#     return x3, x3 % 10


def part2(text: str) -> int:
    secret_numbers = parse(text)
    diff_dict_list = [diff_dict(2000, x) for x in secret_numbers]
    banana_pr_dict = reduce(
        lambda x, y: {
            k: x.get(k, 0) + y.get(k, 0) for k in x.keys() | y.keys()
        },
        diff_dict_list,
    )

    return max(banana_pr_dict.values())


# print("Part 2 test:", part2(test2))
# print("Part 2 real:", part2(data))
