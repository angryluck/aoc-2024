from functools import partial

from aocd import get_data

# Data
data = get_data(year=2024, day=24)

test = """\
x00: 1
x01: 1
x02: 1
y00: 0
y01: 1
y02: 0

x00 AND y00 -> z00
x01 XOR y01 -> z01
x02 OR y02 -> z02\
"""


test2 = """\
x00: 1
x01: 0
x02: 1
x03: 1
x04: 0
y00: 1
y01: 1
y02: 1
y03: 1
y04: 1

ntg XOR fgs -> mjb
y02 OR x01 -> tnw
kwq OR kpj -> z05
x00 OR x03 -> fst
tgd XOR rvg -> z01
vdt OR tnw -> bfw
bfw AND frj -> z10
ffh OR nrd -> bqk
y00 AND y03 -> djm
y03 OR y00 -> psh
bqk OR frj -> z08
tnw OR fst -> frj
gnj AND tgd -> z11
bfw XOR mjb -> z00
x03 OR x00 -> vdt
gnj AND wpb -> z02
x04 AND y00 -> kjc
djm OR pbm -> qhw
nrd AND vdt -> hwm
kjc AND fst -> rvg
y04 OR y02 -> fgs
y01 AND x02 -> pbm
ntg OR kjc -> kwq
psh XOR fgs -> tgd
qhw XOR tgd -> z09
pbm OR djm -> kpj
x03 XOR y03 -> ffh
x00 XOR y04 -> ntg
bfw OR bqk -> z06
nrd XOR fgs -> wpb
frj XOR qhw -> z04
bqk OR frj -> z07
y03 OR x01 -> nrd
hwm AND bqk -> z03
tgd XOR rvg -> z12
tnw OR pbm -> gnj\
"""

type Wire = str
type WireState = dict[Wire, int]
type Command = str
type Gates = dict[Wire, tuple[Command, Wire, Wire]]


# Convert data (text) to workable input
def parse(text: str) -> tuple[WireState, Gates]:
    wire_dict = {}
    wires, gates = text.split("\n\n")
    for line in wires.split("\n"):
        w, i = line.split(": ")
        wire_dict[w] = int(i)

    gate_dict = {}
    for line in gates.split("\n"):
        w1, logic, w2, _, w3 = line.split(" ")
        gate_dict[w3] = (logic, w1, w2)
    return wire_dict, gate_dict


def do_command(command: Command, x: int, y: int) -> int:
    match command:
        case "OR":
            return x | y
        case "AND":
            return x & y
        case "XOR":
            return x ^ y
        case _:
            raise ValueError


# Mutates wire_state with new result, recursively
def set_value(wire_state: WireState, gates: Gates, wire: Wire) -> int:
    """Compute the value of a given wire.

    Also updates wire_state to record the new values.
    """
    getter = partial(set_value, wire_state, gates)
    if wire in wire_state:
        return wire_state[wire]
    cmd, w1, w2 = gates[wire]
    wire_state[wire] = do_command(cmd, getter(w1), getter(w2))
    return wire_state[wire]


# Part 1


def debug1(text: str) -> None:
    wire_dict, gate_dict = parse(text)
    print(set_value(wire_dict, gate_dict, "gnj"))


# debug1(test2)
def get_number(bits: list[int]) -> int:
    # bits should be list of 1's and 0's
    return sum(b * (2**p) for b, p in zip(bits, range(len(bits))))


def part1(text: str) -> int:
    wires, gates = parse(text)
    for w in gates:
        set_value(wires, gates, w)
    z_list = []
    for k, v in wires.items():
        if k.startswith("z"):
            z_list.append((k, v))
    z_list.sort()
    return get_number([z[1] for z in z_list])


print(f"Part 1 test:\n{part1(test)}")
print(f"Part 1 test2:\n{part1(test2)}")
print(f"Part 1 real:\n{part1(data)}")


# Part 2
type RecGate = tuple[RecGate, Command, RecGate] | Wire
type GateState = dict[Wire, RecGate]


def parse2(text: str) -> tuple[GateState, Gates]:
    gate_state_dict = {}
    wires, gates = text.split("\n\n")
    for line in wires.split("\n"):
        w, i = line.split(": ")
        gate_state_dict[w] = w

    gate_dict = {}
    for line in gates.split("\n"):
        w1, logic, w2, _, w3 = line.split(" ")
        gate_dict[w3] = (logic, w1, w2)
    return gate_state_dict, gate_dict


def set_gate(gate_state: GateState, gates: Gates, wire: Wire) -> RecGate:
    """Compute the value of a given wire.

    Also updates wire_state to record the new values.
    """
    getter = partial(set_gate, gate_state, gates)
    if wire in gate_state:
        return gate_state[wire]
    cmd, w1, w2 = gates[wire]
    gate_state[wire] = (getter(w1), cmd, getter(w2))
    return gate_state[wire]


def compute_rec_gate(gate_nr: str, rec_gate: RecGate) -> int:
    """Compute value of rec_gate if xi and yi is set to 1."""
    fun = partial(compute_rec_gate, gate_nr)
    match rec_gate:
        case (w1, cmd, w2):
            return do_command(cmd, fun(w1), fun(w2))
        case w if w in (f"x{gate_nr}", f"y{gate_nr}"):
            return 1
        case _:
            return 0


def part2(text: str) -> int:
    gate_state, gates = parse2(text)
    for w in gates:
        set_gate(gate_state, gates, w)
    zs = sorted(x for x in gate_state if x.startswith("z"))
    print(gate_state[zs[1]])
    # for z, i in zip(zs, range(len(zs))):
    #     print(z, end=", ")
    #     print(i, end=", ")
    #     print(compute_rec_gate(str(i).zfill(2), gate_state[z]))

    # for x in [1, 2, 3, 4, 5]:
    #     print(compute_rec_gate(f"0{x}", g))
    return 0


part2(data)
# print(f"Part 2 test:\n{part2(test)}")
# print(f"Part 2 real:\n{part2(data)}")
