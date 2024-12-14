from aocd import get_data

# Data
data = get_data(year=2024, day=1)

test = """
3   4
4   3
2   5
1   3
3   9
3   3
"""


# Convert data to workable list
def parse(text: str) -> tuple[list[int], list[int]]:
    all_vals = [int(i) for i in text.split()]
    return sorted(all_vals[::2]), sorted(all_vals[1::2])


# Part 1
def total_distance(xs: list[int], ys: list[int]) -> int:
    return sum(abs(x - y) for (x, y) in zip(xs, ys))


def part1(text: str) -> int:
    (l1, l2) = parse(text)
    return total_distance(l1, l2)


print(part1(test))
print(part1(data))


# Part 2
def similarity(x: int, xs: list[int]) -> int:
    return x * xs.count(x)


def total_similarity(xs: list[int], ys: list[int]) -> int:
    return sum(similarity(x, ys) for x in xs)


def part2(text: str) -> int:
    (l1, l2) = parse(text)
    return total_similarity(l1, l2)


print(part2(test))
print(part2(data))
