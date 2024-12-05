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

# Add rule to dictionary
def parse_rule(text:str)->():
    p1, p2 = (int(i) for i in text.split("|"))
    # NOTE: Never run, so doesn't work
    # (rules.setdefault(p,set()) for p in [p1, p2])
    for p in p1, p2:
        RULES.setdefault(p,set())
    RULES[p1].add(p2)

# Convert data (text) to workable input
def parse(text:str) -> [int]:
    text_split = text.split("\n\n")
    rule_lines = text_split[0].split("\n")
    for rule in rule_lines:
        # Adding pair to dict RULE
        parse_rule(rule)
    update_lines = text_split[1].split("\n")
    return [[int(i) for i in line.split(",")] for line in update_lines]

## lt p1 p2 == p1 < p2 (p1 should be to the left of p2 in list)
def lt(p1:int, p2:int) -> bool:
    return p2 in RULES[p1]


# Part 1
def is_in_order(update: [int]) -> bool:
    return all(all(lt(p1, p2) for p2 in update[i+1:])
               for i, p1 in enumerate(update))


def middle_page_number(xs: [int]) -> int:
    return xs[len(xs)//2]

def part1(text:str) -> int:
    updates = parse(text)
    return sum(middle_page_number(update)
               for update in updates
               if is_in_order(update))

print(part1(test))
print(part1(data))

# Part 2
def part2(text:str) -> int:
    (rules, updates) = parse(text)
    sorter = (lambda p1, p2: lt(p1, p2))
    return sum(middle_page_number(sorted(update, key=sorter))
               for update in updates
               if not is_in_order(rules, update))

print(part2(test))
print(part2(data))
