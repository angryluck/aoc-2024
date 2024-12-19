from typing import Any

from aocd import get_data

from util import Matrix, Index, add, sub, scale, print_path

# Data
data = get_data(year=2024, day=8)

test = """\
............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............\
"""

type Frequency = str  # Only a char


# Convert data (text) to workable input
def parse(text: str) -> tuple[Matrix, dict[Frequency, list[Index]]]:
    matrix = Matrix(text)
    freq_dict = {}
    for index in matrix.indices():
        if (frequency := matrix.entry(index)) and (frequency != "."):
            freq_dict.setdefault(frequency, [])
            freq_dict[frequency].append(index)
    return Matrix(text), freq_dict


# Part 1
def antinode_pair(index1: Index, index2: Index) -> set[Index]:
    diff = sub(index2, index1)
    an1 = add(index2, diff)
    diff = scale(-1, diff)
    an2 = add(index1, diff)
    return {an1, an2}


def antinodes_freq(freq_indices: list[Index]) -> set[Index]:
    antinodes = set()
    for i in range(len(freq_indices)):
        fi1 = freq_indices[i]
        for fi2 in freq_indices[i + 1 :]:
            antinodes.update(antinode_pair(fi1, fi2))
    return antinodes


def antinodes_all(
    matrix: Matrix, freq_dict: dict[Frequency, list[Index]]
) -> set[Index]:
    antinodes = set()
    for freq_list in freq_dict.values():
        antinodes.update(antinodes_freq(freq_list))
    valid_indices = set(matrix.indices())
    return antinodes & valid_indices


def part1(text: str) -> int:
    matrix, freq_dict = parse(text)
    # print(antinodes_all(matrix, freq_dict))
    antinodes_all(matrix, freq_dict)
    return len(antinodes_all(matrix, freq_dict))


print("Part 1 test:", part1(test))
print("Part 1 real:", part1(data))


# Part 2
def antinode_line(index1: Index, index2: Index, max_size: int) -> set[Index]:
    diff = sub(index2, index1)
    antinodes = set()
    tmp = index2
    for _ in range(max_size):
        antinodes.add(tmp)
        tmp = add(tmp, diff)
    diff = scale(-1, diff)
    tmp = index1
    for _ in range(max_size):
        antinodes.add(tmp)
        tmp = add(tmp, diff)
    return antinodes


def antinodes_freq_2(freq_indices: list[Index], max_size: int) -> set[Index]:
    antinodes = set()
    for i in range(len(freq_indices)):
        fi1 = freq_indices[i]
        for fi2 in freq_indices[i + 1 :]:
            antinodes.update(antinode_line(fi1, fi2, max_size))
    return antinodes


def antinodes_all_2(
    matrix: Matrix, freq_dict: dict[Frequency, list[Index]]
) -> set[Index]:
    antinodes = set()
    valid_indices = set(matrix.indices())
    for freq_list in freq_dict.values():
        antinodes.update(
            antinodes_freq_2(freq_list, max(matrix.rows, matrix.cols))
        )
        # print_path(matrix, antinodes & valid_indices, char="#")
    return antinodes & valid_indices


def part2(text: str) -> int:
    matrix, freq_dict = parse(text)
    return len(antinodes_all_2(matrix, freq_dict))


print("Part 2 test:", part2(test))
print("Part 2 real:", part2(data))
