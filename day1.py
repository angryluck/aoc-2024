from aocd import get_data

data = get_data(year=2024, day=1)

test = """
3   4
4   3
2   5
1   3
3   9
3   3
"""

def parse(text:str) -> ([int],[int]):
    all_vals = [int(i) for i in text.split()]
    return sorted(all_vals[::2]), sorted(all_vals[1::2])

def total_distance(xs:[int], ys:[int]) -> int:
    return sum(abs(x-y) for (x,y) in zip(xs, ys))

def part1(text:str) -> int:
    (l1, l2) = parse(text)
    return total_distance(l1, l2)

print(part1(test))
print(part1(data))

def similarity(x:int, xs:[int]) -> int:
    return x * xs.count(x)

def total_similarity(xs:[int], ys:[int]) -> int:
    return sum(similarity(x,ys) for x in xs)

def part2(text:str) -> int:
    (l1, l2) = parse(text)
    return total_similarity(l1, l2)

print(part2(test))
print(part2(data))
