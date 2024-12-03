import pyparsing as pp
from aocd import get_data
from pyparsing import (
    Char,
    CharsNotIn,
    Literal,
    Suppress,
    Word,
    nums,
    pyparsing_common,
)

# Data
data = get_data(year=2024, day=3)

# Part 1
test = "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"

# Has to be first! Doesn't skip whitespace
pp.ParserElement.set_default_whitespace_chars("")

# Shorthand
lpar, rpar, comma = map(Suppress, "(),")
num = Word(nums,max=3).setParseAction(pyparsing_common.convertToInteger)
pair = (lpar + num + comma + num + rpar).setParseAction(lambda t: (t[0], t[1]))
mul = Suppress("mul") + pair

skip = Suppress(CharsNotIn("m"))
m = Suppress(Char("m"))
parser = (skip | mul | m)[1,...]


# Convert data (text) to workable input
def parse(text:str) -> [(int,int)]:
    return parser.parseString(text)

def part1(text:str) -> int:
    vals = parse(text)
    return sum(x*y for (x,y) in vals)

print(part1(test))
print(part1(data))


# Part 2
test2="xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"
do = Literal("do()")
dont = Literal("don't()")

skip2 = Suppress(CharsNotIn("md"))
md = Suppress(Char("md"))
parser2 = (skip2 | do | dont | mul | md)[1,...]

def part2(text:str) -> int:
    vals = parser2.parseString(text)
    enabled = True
    total = 0
    # print(vals)
    for t in vals:
        if t == "do()":
            enabled = True
            continue
        if t == "don't()":
            enabled = False
            continue
        if enabled:
            x,y = t[0], t[1]
            total += x*y
    return total

print(part2(test2))
print(part2(data))
