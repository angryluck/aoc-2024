from aocd import get_data

# Data
data = get_data(year=2024, day=7)

test = """\
190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20"""

type Equation = tuple[int, list[int]]


# Convert data (text) to workable input
def parse_line(text: str) -> Equation:
    text_split = text.split(": ")
    val = int(text_split[0])
    nums = [int(num) for num in text_split[1].split(" ")]
    return (val, nums)


def parse(text: str) -> list[Equation]:
    return [parse_line(line) for line in text.split("\n")]


def is_valid(eq: Equation) -> bool:
    val, nums = eq
    possible_vals = {nums[0]}
    for num in nums[1:]:
        new_add = {x + num for x in possible_vals}
        new_mult = {x * num for x in possible_vals}
        possible_vals = new_add | new_mult
    return val in possible_vals


# Part 1
def part1(text: str) -> int:
    equations = parse(text)
    return sum(eq[0] for eq in equations if is_valid(eq))


print("Part 1 test:", part1(test))
print("Part 1 real:", part1(data))


# Part 2
def is_valid_2(eq: Equation) -> bool:
    val, nums = eq
    possible_vals = {nums[0]}
    for num in nums[1:]:
        new_add = {x + num for x in possible_vals}
        new_mult = {x * num for x in possible_vals}
        ## SHOULDNT CONCAT THE WHOLE THING! ...
        # Nvm, misread the task, lolol
        new_concat = {int(str(x) + str(num)) for x in possible_vals}
        possible_vals = new_add | new_mult | new_concat
    return val in possible_vals


def part2(text: str) -> int:
    equations = parse(text)
    return sum(eq[0] for eq in equations if is_valid_2(eq))


print("Part 2 test:", part2(test))
print("Part 2 real:", part2(data))
