from aocd import get_data

# Data
data = get_data(year=2024, day=23)

test = """\
kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn\
"""

type Computer = str
# Direction doesn't matter
type Connections = dict[Computer, set[Computer]]


# Convert data (text) to workable input
def parse(text: str) -> Connections:
    connections = {}
    lines = text.split("\n")
    for line in lines:
        c1, c2 = line.split("-")
        connections.setdefault(c1, set()).add(c2)
        connections.setdefault(c2, set()).add(c1)

    return connections


def triples(
    connections: Connections, computer: Computer
) -> set[frozenset[Computer]]:
    triples = set()
    connected = connections[computer]
    for c2 in connected:
        conn2 = connections[c2]
        triples.update(
            frozenset({computer, c2, c3}) for c3 in connected & conn2
        )
    return triples


def all_triples(connections: Connections) -> set[frozenset[Computer]]:
    ret = set()
    for key in connections:
        ret.update(triples(connections, key))

    return ret


# Part 1


def contains_t(triple: frozenset[Computer]) -> bool:
    return any(x[0] == "t" for x in triple)


def part1(text: str) -> int:
    connections = parse(text)
    triples = all_triples(connections)
    valid_triples = {x for x in triples if contains_t(x)}
    return len(valid_triples)


print("Part 1 test:", part1(test))
print("Part 1 real:", part1(data))


# Part 2
def biggest_lan(connections: Connections, computer: Computer) -> set[Computer]:
    retval = {computer}
    for c in connections[computer]:
        if retval <= connections[computer]:
            {1, 2, 3}
    return set()


# Should only be two computers!
type Pair = frozenset[Computer]


class Network:
    """Dict of computer connections.

    connections: Dictionary of sets of computers a given computer is connected
    to.
    pairs: set of (frozen)sets of pairs of computer connections.
    computers: set of computers
    """

    def __init__(self, text: str):
        self.connections = {}
        self.pairs = set()
        self.computers = set()
        lines = text.split("\n")
        for line in lines:
            c1, c2 = line.split("-")
            self.connections.setdefault(c1, set()).add(c2)
            self.connections.setdefault(c2, set()).add(c1)
            self.pairs.add(frozenset({c1, c2}))
            self.computers.update({c1, c2})

    def extend_group(
        self, group: frozenset[Computer]
    ) -> set[frozenset[Computer]]:
        common = set.intersection(*(self.connections[c] for c in group))
        return {group | {x} for x in common}


def part2(text: str) -> str:
    network = Network(text)
    groups = network.pairs
    count = 3
    while True:
        next_groups = set.union(
            *(set.union(network.extend_group(p)) for p in groups)
        )
        if next_groups == set():
            break
        groups = next_groups
        print(f"Biggest group: size {count}")
        count += 1
    sorted_group = sorted([c for group in groups for c in group])
    return ",".join(sorted_group)


print(f"Part 2 test:\n{part2(test)}")
print(f"Part 2 real:\n{part2(data)}")


def debug(text: str) -> None:
    # pairs = parse_2(text)
    # grp = {"co", "de"}
    # print(can_extend(pairs, grp, "ka"))
    network = Network(text)
    groups = network.pairs
    count = 3
    while True:
        next_groups = set.union(
            *(set.union(network.extend_group(p)) for p in groups)
        )
        if next_groups == set():
            break
        groups = next_groups
        print(f"Group size: {count}")
        count += 1
    print(count)
    print(groups)


# debug(data)
