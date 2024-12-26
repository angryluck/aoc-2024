from __future__ import annotations
from functools import partial

from aocd import get_data

from util import Matrix

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
    """Move boxes in direction if possible, and return new robot position."""
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
    box_coordinates = {i for i in maze.indices() if maze.entry(i) == "O"}
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


class BigWarehouse:
    """Warehouse with walls, big boxes and a robot."""

    def __init__(self, text: str) -> None:
        """Text should be the warehouse part of the data, without instructions."""
        text = (
            text.replace(".", "..")
            .replace("#", "##")
            .replace("O", "[]")
            .replace("@", "@.")
        )
        matrix = Matrix(text)
        boxes = set()
        walls = set()
        robot_position = (-1, -1)
        for i in matrix.indices():
            if matrix.entry(i) == "@":
                robot_position: Position = i
            if matrix.entry(i) == "[":
                boxes.add((i, add(i, (1, 0))))
            if matrix.entry(i) == "#":
                walls.add(i)
        if robot_position == (-1, -1):
            print("Didn't find robot :(")
            raise ValueError
        walls = frozenset(walls)
        self.walls: frozenset[Position] = walls
        self.boxes: set[BigBox] = boxes
        self.robot_position: Position = robot_position
        self.rows: int = matrix.rows
        self.cols: int = matrix.cols

    def __str__(self) -> str:
        output = ""
        for j in range(self.rows):
            for i in range(self.cols):
                if (i, j) in self.walls:
                    char = "#"
                elif (i, j) in {x[0] for x in self.boxes}:
                    char = "["
                elif (i, j) in {x[1] for x in self.boxes}:
                    char = "]"
                elif (i, j) == self.robot_position:
                    char = "@"
                else:
                    char = "."
                output += char
            output += "\n"
        return output

    def is_at_box(self, position: Position) -> None | BigBox:
        """If there is a box at given position, return said box.

        Note that boxes should never overlap, so there is at most **one** box at
        any given position.
        """
        left_box = (position, add(position, (1, 0)))
        if left_box in self.boxes:
            return left_box
        right_box = (add(position, (-1, 0)), position)
        if right_box in self.boxes:
            return right_box
        return None

    def boxes_to_move(
        self, direction: Direction, position: Position
    ) -> None | set[BigBox]:
        """Determine which boxes should be moved.

        Return None if boxes hit a wall, indicating that the robot should not
        move.
        """
        # Default to robot_position, other positions are only for recursive call
        next_position = add(position, direction)
        if next_position in self.walls:
            return None
        box = self.is_at_box(next_position)
        if box is None or position in box:
            return set()  # Right statement is to avoid infinite recursion: If
            # the box from the next position is the same box as the current
            # position, the function would infinitely loop those two
            # positions.

        res = {box}
        for box_position in box:
            next_boxes = self.boxes_to_move(direction, box_position)
            if next_boxes is None:
                return None
            res.update(next_boxes)
        return res

    @staticmethod
    def move_box(direction: Direction, box: BigBox) -> BigBox:
        left_pos, right_pos = box
        return (add(left_pos, direction), add(right_pos, direction))

    def move_robot(self, direction: Direction) -> None:
        """Try to push robot in given direction.

        Updates robot_pos and boxes if successful, otherwise does nothing
        """
        moving_boxes = self.boxes_to_move(direction, self.robot_position)
        if moving_boxes is None:
            return
        self.robot_position = add(self.robot_position, direction)
        # if not (moving_boxes := to_move(walls, boxes, d, robot_pos)):
        #     return robot_pos, boxes
        self.boxes.difference_update(moving_boxes)
        self.boxes.update(
            {self.move_box(direction, box) for box in moving_boxes}
        )

    @staticmethod
    def gps_coordinate_box(box: BigBox) -> int:
        (x, y) = box[0]
        return x + 100 * y

    def value(self) -> int:
        return sum(self.gps_coordinate_box(x) for x in self.boxes)


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


def debug(text: str) -> None:
    matrix, instructions = text.split("\n\n")
    instructions = instructions.replace("\n", "")
    directions = [direction(x) for x in instructions]
    gg = BigWarehouse(matrix)
    print(gg)
    for x in directions[:5]:
        gg.move_robot(x)
    print(gg)


# debug(data)


def part2(text: str) -> int:
    matrix, instructions = text.split("\n\n")
    warehouse = BigWarehouse(matrix)
    instructions = instructions.replace("\n", "")
    directions = [direction(x) for x in instructions]
    for x in directions:
        warehouse.move_robot(x)
    return warehouse.value()


print("Part 2 test:", part2(test))
# print("Part 2 test2:", part2(test2))
# print("Part 2 test3:", part2(test3))
print("Part 2 real:", part2(data))
