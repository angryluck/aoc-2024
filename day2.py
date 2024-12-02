from aocd import get_data

# Data
data = get_data(year=2024, day=2)

test = """
7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
"""

# Convert data to workable list
def parse(text:str) -> [[int]]:
    lines = text.strip().splitlines()
    return [[int(i) for i in line.split()] for line in lines]

def is_safe(xs:[int]) -> bool:
    if len(xs)<=1:
        return True
    is_increasing = xs[0] < xs[-1]
    max_diff = 3
    for i in range(len(xs)-1):
        x1 = xs[i]
        x2 = xs[i+1]
        if (x1 < x2) != is_increasing or abs(x1-x2) > max_diff or x1==x2:
            return False
    return True

def safe_count(xss:[[int]]) -> int:
    return sum(is_safe(xs) for xs in xss)

# Part 1
def part1(text:str) -> int:
    return safe_count(parse(text))

print(part1(test))
print(part1(data))


def is_safe_dampened(xs:[int])->bool:
    if is_safe(xs):
        return True
    return any(is_safe(xs[:i]+xs[i+1:]) for i in range(len(xs)))

def safe_count_dampened(xss:[[int]]) -> int:
    return sum(is_safe_dampened(xs) for xs in xss)

def part2(text:str) -> int:
    return safe_count_dampened(parse(text))

print(part2(test))
print(part2(data))
