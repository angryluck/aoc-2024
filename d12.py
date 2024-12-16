from itertools import product

from aocd import get_data

from util import Matrix, add

# from itertools import reduce

# Data
data = get_data(year=2024, day=12)

test = """\
RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE"""

type Index = tuple[int, int]


# Convert data (text) to workable input
def parse(text: str) -> Matrix:
    return Matrix(text)


# Part 1
def get_region_rec(index: Index, garden: Matrix, visited: set) -> set[Index]:
    current_plant = garden.entry(index)
    if current_plant is None:
        return set()
    visited = visited | {index}
    for step in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        if tmp := garden.move(index, step):
            i, p = tmp
            if p == current_plant and i not in visited:
                visited = get_region_rec(i, garden, visited)
    return visited


def get_region(index: Index, garden: Matrix) -> set[Index]:
    return get_region_rec(index, garden, set())


def get_all_regions(garden: Matrix) -> list[set[Index]]:
    regions = []
    for index in product(range(garden.cols), range(garden.rows)):
        if any(index in region for region in regions):
            continue
        regions.append(get_region(index, garden))

    return regions


# For debugging
def print_region(region: set[Index], garden: Matrix) -> None:
    for j in range(garden.rows):
        for i in range(garden.cols):
            index = (i, j)
            char = garden.entry(index) if index in region else " "
            print(char, end="")
        print()


def area(region: set[Index]) -> int:
    return len(region)


def perimeter(region: set[Index]) -> int:
    # For each index in the region, check if spot above,below,right,left is
    # available, and in that case add 1 to the perimeter (corresponding to a
    # side of the fence)
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    return sum(
        1
        for index, step in product(region, directions)
        if add(index, step) not in region
    )


def price(region: set[Index]) -> int:
    return area(region) * perimeter(region)


def part1(text: str) -> int:
    garden = parse(text)
    regions = get_all_regions(garden)
    return sum(price(x) for x in regions)


print("Part 1 test:", part1(test))
print("Part 1 real:", part1(data))


def rotate(index: Index) -> Index:
    # Rotate 90 degrees counterclockwise
    (i, j) = index
    return (j, -i)


def side_count(direction: Index, region: set[Index]) -> int:
    # First add all the fences of the given direction:
    # for index in region:
    fences = {
        next_index
        for index in region
        if (next_index := add(index, direction)) not in region
    }
    # Now remove all fences but one, in all straight lines
    perp = rotate(direction)  # Perpendicular direction
    return sum(1 for index in fences if add(index, perp) not in fences)


# Part 2
def total_side_count(region: set[Index]) -> int:
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    return sum(side_count(d, region) for d in directions)


def part2(text: str) -> int:
    garden = parse(text)
    regions = get_all_regions(garden)
    return sum(area(x) * total_side_count(x) for x in regions)


print("Part 2 test:", part2(test))
print("Part 2 real:", part2(data))


# def tester(text: str) -> None:
#     gg = parse(text)
#     regions = get_all_regions(gg)
#     region = regions[0]
#     print_region(region, gg)
#     print("-" * 30)
#     print("Area: ", area(region), "Sides: ", all_sides(region))
#     print("=" * 30)


# tester(test)
