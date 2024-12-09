from aocd import get_data

# Data
data = get_data(year=2024, day=6)

test = """\
....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...\
"""

class Field:
    def __init__(self, matrix:[[str]]) -> ():
        self.matrix=matrix
        self.rows=len(matrix)
        self.cols=len(matrix[0])
        self.visited = 0


# Convert data (text) to workable input
def parse(text:str) -> (Field, (int, int)):
    matrix = [list(line) for line in text.split("\n")]
    # rows, cols = (len(M), len(M[0]))
    field = Field(matrix)
    for i in range(field.rows):
        for j in range(field.cols):
            if field.matrix[j][i] == "^":
                field.visited += 1
                field.matrix[j][i] = "X"
                return field, (i, j)
    print("Error: Didn't find start")
    return None


# Part 1
def direction(d:int)->(int, int):
    # d=0,1,2,3 is up, right, down, left
    match d%4:
        case 0:
            return (0,-1)
        case 1:
            return (1,0)
        case 2:
            return (0,1)
        case 3:
            return (-1,0)

# Copilot suggestion: Maybe indexing into an array is faster than mathcing.
DIRECTIONS = [(0,-1), (1,0), (0,1), (-1,0)]

def move(d:int, start:(int,int), field: Field) -> (int, (int, int)):
    nx = (start[0] + direction(d)[0])
    ny = (start[1] + direction(d)[1])
    if nx < 0 or ny < 0 or nx >= field.cols or ny >= field.rows:
        # print("Exited field")
        return d, (-1,-1)
    if field.matrix[ny][nx] == "#":
        # print("Hit wall, turning")
        return (d+1), start
    if field.matrix[ny][nx] == ".":
        field.matrix[ny][nx]="X"
        field.visited += 1
        return d, (nx, ny)
    if field.matrix[ny][nx] == "X":
        return d, (nx, ny)
    return start

def part1(text:str) -> int:
    field, start = parse(text)
    d = 0
    while start != (-1,-1):
        # print(d, start)
        d, start = move(d, start, field)

    # for line in field.matrix:
        # print(line)
    return field.visited

print(part1(test))
print(part1(data))

# print("Part 1 test:", part1(test))
# print("Part 1 real:", part1(data))


# Part 2
def move2(blocked: (int, int), d:int, start:(int,int),
          count: int, field: Field) -> (int, (int, int), int):
    # No mutating for this one
    nx = (start[0] + direction(d)[0])
    ny = (start[1] + direction(d)[1])
    if nx < 0 or ny < 0 or nx >= field.cols or ny >= field.rows:
        return d, (-1,-1), count
    if (nx, ny) == blocked or field.matrix[ny][nx] == "#":
        return (d+1), start, count
    return d, (nx, ny), count+1



def part2(text:str) -> int:
    # Very slow :/
    field, start = parse(text)
    loops = 0
    for y in range(field.rows):
        for x in range(field.cols):
            blocked = (x,y)
            if blocked == start:
                continue
            count = 0
            d = 0
            pos = start
            while pos != (-1, -1):
                d, pos, count = move2(blocked, d, pos, count, field)
                # If the number of spaces visited is larger than columns *
                # rows*4, then we must have visited at least one space 5 times,
                # i.e. at least one space from the same direction twice, i.e. we
                # are in a loop. (But very ineficient to do this so many times)
                if count >= field.cols*field.rows*4:
                    loops += 1
                    print(loops, "loops")
                    break

    return loops

def move2_2(blocked: (int, int), d:int, start:(int,int), visited_count: [[int]],
            field: Field) -> (int, (int, int)):
    # Mutates visited_count
    nx = (start[0] + direction(d)[0])
    ny = (start[1] + direction(d)[1])
    if nx < 0 or ny < 0 or nx >= field.cols or ny >= field.rows:
        return d, (-1,-1)
    if (nx, ny) == blocked or field.matrix[ny][nx] == "#":
        return (d+1), start
    visited_count[ny][nx]+=1
    return d, (nx, ny)

def move2_3(blocked: (int, int), d:int, start:(int,int), visited_count: [[int]],
            field: Field) -> (int, (int, int)):
    # Mutates visited_count
    dx, dy = DIRECTIONS[d%4]
    nx, ny = start[0]+dx, start[1]+dy
    if nx < 0 or ny < 0 or nx >= field.cols or ny >= field.rows:
        return d, (-1,-1)
    if (nx, ny) == blocked or field.matrix[ny][nx] == "#":
        return (d+1), start
    visited_count[ny][nx]+=1
    return d, (nx, ny)



def part2_2(text:str) -> int:
    field, start = parse(text)
    loops = 0
    max_visit=5

    # Run algorithm from part 1, so we get X wherever the man has visited. These
    # are the only possible places to put an obstacle!
    d=0
    pos = start
    while pos != (-1,-1):
        d, pos = move(d, pos, field)
    # for line in field.matrix:
    #     print(line)
    for y in range(field.rows):
        for x in range(field.cols):
            blocked = (x,y)
            # Only blocking on an 'X' can change anything
            if blocked == start or field.matrix[y][x] in {"#", "."}:
                continue
            # If we have visited a spot 5 times, then we have visited it from
            # one direction at least 2 times, so a loop.
            # We could also save the directions visited with, rather than a
            # count, but then we lose time by having to do a string comparison
            # every step, rather than just increment a value.
            # BUG: THIS ACTS WEIRD, RIP PYTHON ;(
            # visited_count = [[0]*field.cols]*field.rows
            visited_count = [[0 for _ in range(field.cols)] for _ in
                             range(field.rows)]
            d = 0
            (nx,ny) = start
            while (nx, ny) != (-1, -1) and visited_count[ny][nx]<max_visit:
                d, (nx,ny) = move2_3(blocked, d, (nx,ny),
                                          visited_count, field)
            if visited_count[ny][nx] == max_visit:
                loops += 1
                print(loops, "loops")
    return loops




# print("Part 2 test:", part2(test))
# print("Part 2 real:", part2(data))
print("Part 2 test, v2:", part2_2(test))
print("Part 2 real, v2:", part2_2(data))
