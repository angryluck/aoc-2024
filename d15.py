from functools import partial
from typing import Any
from util import Matrix, print_path
from aocd import get_data

# Data
data = get_data(year=2024, day=15)

test = """\
##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^
"""


test2 = """\
########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

<^^>>>vv<v>>v<<"""


type Position = tuple[int, int]
type Direction = tuple[int, int]


def direction(char: str) -> Direction:
    match char:
        case "^":
            return (0, -1)
        case ">":
            return (1, 0)
        case "<":
            return (-1, 0)
        case "v":
            return (0, 1)
    raise ValueError


# Convert data (text) to workable input
def parse(text: str) -> tuple[Matrix, Position, list[Direction]]:
    matrix, instructions = text.split("\n\n")
    matrix = Matrix(matrix)
    robot_pos = (-1, -1)
    for i in matrix.indices():
        if matrix.entry(i) == "@":
            robot_pos = i
            break
    instructions = list(instructions.replace("\n", ""))
    directions = [direction(i) for i in instructions]
    return matrix, robot_pos, directions


def add(p: Position, d: Direction) -> Position:
    (x, y), (dx, dy) = p, d
    return (x + dx, y + dy)


def move(matrix: Matrix, d: Direction, robot_pos: Position) -> Position:
    """Tries to move boxes, but changes nothing if impossible. Returns new
    robot position."""
    next_pos = add(robot_pos, d)
    free_pos = next_pos
    while matrix.entry(free_pos) == "O":
        free_pos = add(free_pos, d)
    match matrix.entry(free_pos):
        case "#":
            return robot_pos
        case ".":
            matrix.set(free_pos, "O")
            matrix.set(next_pos, "@")
            matrix.set(robot_pos, ".")
            return next_pos
        case _:
            raise ValueError


def gps_coordinate(pos: Position) -> int:
    (x, y) = pos
    return x + 100 * y


def part1(text: str) -> int:
    maze, robot_pos, instructions = parse(text)
    mover = partial(move, maze)
    for i in instructions:
        robot_pos = mover(i, robot_pos)
    box_coordinates = set(i for i in maze.indices() if maze.entry(i) == "O")
    return sum(gps_coordinate(x) for x in box_coordinates)


print("Part 1 test:", part1(test))
print("Part 1 test2:", part1(test2))
print("Part 1 real:", part1(data))


# Part 2
# Set of precisely 2 positions
type BigBox = tuple[Position, Position]


# tuple[Matrix, Position, set[BigBox]]:
def parse2(
    text: str,
) -> tuple[Matrix, frozenset[Position], Position, set[BigBox], list[Direction]]:
    matrix, instructions = text.split("\n\n")
    matrix = matrix.replace(".", "..")
    matrix = matrix.replace("#", "##")
    matrix = matrix.replace("O", "[]")
    matrix = matrix.replace("@", "@.")
    matrix = Matrix(matrix)
    robot_pos = (-1, -1)
    boxes = set()
    walls = set()
    for i in matrix.indices():
        if matrix.entry(i) == "@":
            robot_pos = i
        if matrix.entry(i) == "[":
            boxes.add((i, add(i, (1, 0))))
        if matrix.entry(i) == "#":
            walls.add(i)
    walls = frozenset(walls)
    instructions = list(instructions.replace("\n", ""))
    directions = [direction(i) for i in instructions]
    return matrix, walls, robot_pos, boxes, directions


test3 = """\
#######
#...#.#
#.....#
#..OO@#
#..O..#
#.....#
#######

<vv<<^^<<^^\
"""


def move_box(d: Direction, box: BigBox) -> BigBox:
    lb, rb = box
    return (add(lb, d), add(rb, d))


# Separate move functions for left-right and up-down
def to_move(
    walls: frozenset[Position], boxes: set[BigBox], d: Direction, current_pos: Position
) -> None | set[BigBox]:
    next_pos = add(current_pos, d)
    if next_pos in walls:
        return None
    left_box = (add(next_pos, (-1, 0)), next_pos)
    right_box = (next_pos, add(next_pos, (1, 0)))
    # nnext_pos = add(next_pos, step)
    mover = partial(to_move, walls, boxes, d)
    # box = (next_pos, nnext_pos) if d == 1 else (nnext_pos, next_pos)
    # print(box)
    if left_box in boxes:
        next_box = left_box
    elif right_box in boxes:
        next_box = right_box
    else:
        return set()
    res = {next_box}
    for pos in next_box:
        if pos != current_pos:
            next_boxes = mover(pos)
            if next_boxes is None:
                return None
            res = res | next_boxes
    return res


def debug():
    matrix, walls, robot_pos, boxes, directions = parse2(test3)
    # print(gboxes, gpos)
    if moving := to_move(walls, boxes, (0, -1), (6, 5)):
        print(moving)
        print({move_box((-1, 0), b) for b in moving})


debug()


# def to_move_ud(
#     walls: frozenset[Position], boxes: set[BigBox], d: int, current_pos: Position
# ) -> None:
# return


def move_robot_2(
    walls: frozenset[Position],
    boxes: set[BigBox],
    d: Direction,
    robot_pos: Position,
) -> tuple[Position, set[BigBox]]:
    moving_boxes = to_move(walls, boxes, d, robot_pos)
    if moving_boxes is None:
        return (robot_pos, boxes)
    # if not (moving_boxes := to_move(walls, boxes, d, robot_pos)):
    #     return robot_pos, boxes
    moved_boxes = {move_box(d, box) for box in moving_boxes}
    new_boxes = (boxes - moving_boxes) | moved_boxes
    new_pos = add(robot_pos, d)
    return (new_pos, new_boxes)


def gps_coordinate_box(box: BigBox) -> int:
    (x, y) = box[0]
    return x + 100 * y


def part2(text: str) -> int:
    matrix, walls, robot_pos, boxes, directions = parse2(text)
    print(matrix)
    mover = partial(move_robot_2, walls)
    for d in directions:
        matrix.set(robot_pos, ".")
        (robot_pos, boxes) = mover(boxes, d, robot_pos)
        matrix.set(robot_pos, "@")
        # print_path(matrix, {b[0] for b in boxes})
    return sum(gps_coordinate_box(x) for x in boxes)


print("Part 2 test:", part2(test))
# print("Part 2 test2:", part2(test2))
# print("Part 2 test3:", part2(test3))
print("Part 2 real:", part2(data))
