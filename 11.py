import math
from functools import cache

from aocd import get_data

# Data
data = get_data(year=2024, day=11)

# test = "0 1 10 99 999"
test = "125 17"


# Convert data (text) to workable input
def parse(text: str) -> list[int]:
    # return text.split(" ")
    return [int(num) for num in text.split(" ")]


# Part 1


def transform(num: int) -> list[int]:
    if num == 0:
        return [1]
    digit_string = str(num)
    digits = len(digit_string)
    if digits % 2 == 0:
        return [
            int(digit_string[: digits // 2]),
            int(digit_string[digits // 2 :]),
        ]
    return [int(num) * 2024]


def blink(xs: list[int]) -> list[int]:
    ret = []
    for num in xs:
        ret.extend(transform(num))
    return ret


def part1(text: str) -> int:
    stones = parse(text)
    for _ in range(25):
        stones = blink(stones)
        # print(stones)
    return len(stones)


# print("Part 1 test:", part1(test))
# print("Part 1 real:", part1(data))


# Part 2
# For a given number, what does the computation on it return
FOLLOWS: dict[int, list[int]] = {0: [1]}


def transform2(num: int) -> list[int]:
    # if num == 0:
    #     return [1]
    digits = int(math.log10(num)) + 1
    if digits % 2 == 0:
        tmp = digits // 2
        right = num % (10**tmp)
        left = num // (10**tmp)
        return [left, right]
    return [num * 2024]


def blink2(xs: list[int]) -> list[int]:
    ret = []
    for num in xs:
        if num in FOLLOWS:
            ret.extend(FOLLOWS[num])
        else:
            result = transform2(num)
            FOLLOWS[num] = result
            ret.extend(result)
    return ret


CACHE: dict[tuple[int, int], int] = {}


def stone_count_manual(n: int, x: int) -> int:
    # n: number of iterations to loop over
    # x: Starting stone value
    # Using a hand-made cache-directory to avoid recomputing (utilizing that
    # reading from a dictionary is O(1) in python)
    if n == 0:
        return 1
    if count := CACHE.get((n, x)):
        return count
    if x == 0:
        return CACHE.setdefault((n, x), stone_count_manual(n - 1, 1))
        # return stone_count(n-1, 1)
    digits = int(math.log10(x)) + 1
    if digits % 2 == 0:
        tmp = digits // 2
        right = x % (10**tmp)
        left = x // (10**tmp)
        return CACHE.setdefault(
            (n, x),
            stone_count_manual(n - 1, right) + stone_count_manual(n - 1, left),
        )
    return CACHE.setdefault((n, x), stone_count_manual(n - 1, x * 2024))


@cache
def stone_count_automatic(n: int, x: int) -> int:
    # n: number of iterations to loop over
    # x: Starting stone value
    # Utilizing the functools 'cache' command, which behind the scenes does
    # something close to the manual implementation above
    if n == 0:
        return 1
    if x == 0:
        return stone_count_manual(n - 1, 1)
    digits = int(math.log10(x)) + 1
    if digits % 2 == 0:
        tmp = digits // 2
        right = x % (10**tmp)
        left = x // (10**tmp)
        return stone_count_manual(n - 1, right) + stone_count_manual(
            n - 1, left
        )
    return stone_count_manual(n - 1, x * 2024)


def part2(text: str) -> tuple[int, int]:
    stones = parse(text)
    manual_val = sum(stone_count_manual(75, x) for x in stones)
    auto_val = sum(stone_count_automatic(75, x) for x in stones)
    return (manual_val, auto_val)


print("Part 2 test:", part2(test))
print("Part 2 real:", part2(data))
print(len(CACHE))
