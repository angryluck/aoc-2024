from functools import cache
from typing import Any

from aocd import get_data, partial

# Data
data = get_data(year=2024, day=19)

test = """\
r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb\
"""

type Towel = str
type TowelPattern = str


def towel_combi_possible(
    available_towels: frozenset[Towel],
    pattern: TowelPattern,
    current_towel: Towel = "",
) -> bool:
    current_towel += pattern[0]
    remaining_pattern = pattern[1:]
    # We always pass available_towels and remaining_pattern to the function,
    # only variable that varies is the current_towel
    next_step = partial(
        towel_combi_possible, available_towels, remaining_pattern
    )
    if current_towel in available_towels:
        if remaining_pattern == "":
            return True
        return next_step(current_towel) or next_step("")
    if remaining_pattern == "":
        return False

    return next_step(current_towel)


# Convert data (text) to workable input
def parse(text: str) -> tuple[frozenset[Towel], list[TowelPattern]]:
    split = text.split("\n\n")
    # Frozen set so we can use '@cache' in part 2
    towels = frozenset(t.strip() for t in split[0].split(","))
    combis = split[1].split("\n")
    return towels, combis


# Part 1


def part1(text: str) -> int:
    towels, combis = parse(text)
    count = 0
    for c in combis:
        if towel_combi_possible(towels, c):
            count += 1
    return count


print("Part 1 test:", part1(test))
print("Part 1 real:", part1(data))


@cache
def step(
    available_towels: frozenset[Towel], pattern: TowelPattern, start: int = 0
) -> list[int]:
    return [len(t) for t in available_towels if pattern.startswith(t, start)]


# Part 2
@cache  # OP
def towel_combi_count(
    available_towels: frozenset[Towel], pattern: TowelPattern, start: int = 0
) -> int:
    if pattern[start:] == "":
        return 1
    if step(available_towels, pattern, start) == []:
        return 0
    return sum(
        towel_combi_count(available_towels, pattern, start + s)
        for s in step(available_towels, pattern, start)
    )


def part2(text: str) -> int:
    towels, combis = parse(text)
    count = 0
    for c in combis:
        print(c)
        count += towel_combi_count(towels, c)
    return count


print("Part 2 test:", part2(test))
print("Part 2 real:", part2(data))
