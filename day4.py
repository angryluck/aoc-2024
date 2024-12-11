import pyparsing as pp
from aocd import get_data

# Data
data = get_data(year=2024, day=4)

test = """MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX"""

# Convert data (text) to workable input
def parse(text:str)->None:
    return (text).splitlines()
xmas = pp.Literal("XMAS")
skipbig = pp.Suppress(pp.CharsNotIn("X"))

find_xmas = (skipbig | xmas | pp.Suppress("X"))[1,...]

# print(find_xmas.parse_string(parse(data)[0]))

# Part 1

def diagonal1(t:str, i:int, j:int) -> str:
    # (i,j) is start, at least one of them should be 0
    return ""





def chunks(t:[str]) -> [[str]]:
    # i row, j column, t list of lines of text
    rows = len(t)
    cols = len(t[0])
    right = t
    left = [line[::-1] for line in t]
    up = [ "".join(t[j][i] for j in range(rows)) for i in range(cols)]
    down = [ line[::-1] for line in up]
    # Diagonals are very scuffed, should be made more readable
    dr = []
    for i in range(cols):
        diag = "".join(t[j][i+j] for j in range(rows-i))
        dr.append(diag)
    for j in range(1, rows):
        diag = "".join(t[j+i][i] for i in range(cols-j))
        dr.append(diag)
    ul = [line[::-1] for line in dr]
    dl = []
    for i in range(cols):
        diag = "".join(t[j][i-j] for j in range(i+1))
        dl.append(diag)
    for j in range(1, rows):
        diag = "".join(t[j+i][cols-1-i] for i in range(rows-j))
        dl.append(diag)

    ur = [line[::-1] for line in dl]

    return [right, left, up, down, dr, ul, dl, ur]



def part1(text:str) -> int:
    text_lines = parse(text)
    cks =  chunks(text_lines)
    return sum (len(find_xmas.parse_string(line)) for lines in chunks(text_lines)
         for line in lines)



    # return

print(part1(test))
print(part1(data))


# Part 2
def is_x_mas(t:[str], i:int, j:int) -> bool:
    ul = t[j-1][i-1]
    ur = t[j-1][i+1]
    dr = t[j+1][i+1]
    dl = t[j+1][i-1]
    chars = [ul, ur, dr, dl]
    # No, now we can have
    # M . S
    # . A .
    # S . M
    # long line xd
    return chars.count("M") == 2 and chars.count("S") == 2 and ur != dl and dr != ul and t[j][i] == "A"

def part2(text:str) -> int:
    text_lines = parse(text)
    rows = len(text_lines)
    cols = len(text_lines[0])
    return sum(is_x_mas(text_lines, i, j) for i in range(1, cols-1)
                                    for j in range(1, rows-1))

print(part2(test))
print(part2(data))
