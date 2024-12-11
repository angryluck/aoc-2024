from aocd import get_data

# Data
data = get_data(year=2024, day=5)

test = """47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47"""

# Global variable keeping track of rules. Should ONLY be updated at start, when
# parsing data!
RULES: {int:{int}} = {}
type Rules = {int:{int}}
type Updates = [[int]]
# Add rule to dictionary
def parse_rule(rules: Rules, text:str)->():
    p1, p2 = (int(i) for i in text.split("|"))
    # NOTE: Never run, so doesn't work
    # (rules.setdefault(p,set()) for p in [p1, p2])
    for p in p1, p2:
        rules.setdefault(p,set())
    rules[p1].add(p2)
    return rules

# Convert data (text) to workable input
def parse(text:str) -> (Rules, Updates):
    text_split = text.split("\n\n")
    rule_lines = text_split[0].split("\n")
    rules = {}
    for rule in rule_lines:
        # Adding pair to dict RULE
        parse_rule(rules, rule)
    update_lines = text_split[1].split("\n")
    updates = [[int(i) for i in line.split(",")] for line in update_lines]
    return rules, updates

## lt p1 p2 == p1 < p2 (p1 should be to the left of p2 in list)
def lt(rules:Rules, p1:int, p2:int) -> bool:
    return p2 in rules[p1]


# Part 1
def is_in_order(rules: Rules, updates: Updates) -> bool:
    return all(all(lt(rules, p1, p2) for p2 in updates[i+1:])
               for i, p1 in enumerate(updates))


def middle_page_number(xs: [int]) -> int:
    return xs[len(xs)//2]

def part1(text:str) -> int:
    rules, updates = parse(text)
    return sum(middle_page_number(update)
               for update in updates
               if is_in_order(rules, update))

print("Part 1 test:", part1(test))
print("Part 1 real:",  part1( data))

def move_forward(i:int, xs:[]) -> None:
    tmp1 = xs[i]
    tmp2 = xs[i-1]
    xs[i] = tmp2
    xs[i-1] = tmp1

def sort(rules: Rules, xs: [int]) -> [int]:
    ret = list(xs)
    for i in range(1, len(xs)):
        j = i
        while j>0 and lt(rules, ret[j], ret[j-1]):
            move_forward(j, ret)
            j -= 1
    return ret


# Part 2
def part2(text:str) -> int:
    rules, updates = parse(text)
    # sorter = (lambda p1, p2: lt(p1, p2))
    updates_not_in_order = filter(lambda x : not is_in_order(rules, x), updates)
    return sum(middle_page_number(sort(rules, line))
               for line in updates_not_in_order)

print("Part 2 test:", part2(test))
print("Part 2 real:", part2(data))
