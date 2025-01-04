from __future__ import annotations

from aocd import get_data

# Data
data = get_data(year=2024, day=24)

# PART 2
type Command = str


def do_command(command: Command, x: int, y: int) -> int:
    match command:
        case "OR":
            return x | y
            # return 0
        case "AND":
            return x & y
            # return 0
        case "XOR":
            return x ^ y
            # return 0
        case _:
            raise ValueError


type Wire = str


# For saving in dict-info
class Gate:
    """Store how wire is set.

    Do it like this, and store them in a dict, so we can easily update one gate.
    (Rather than recusively defining the Gate-values all the way down to xi and
    yi).
    Left and right are stored together in a frozenset so
        1. Gates are easily compared (using commutativity of XOR, AND and OR)
        2. The gates are hashable, so we can do quick lookups on a given wire
        matching a gate.
    """

    def __init__(self, left: Wire, op: Command, right: Wire) -> None:
        self.op = op
        if left == right:
            raise ValueError
        self.inputs = frozenset({left, right})

    def __str__(self) -> str:
        left, right = tuple(self.inputs)
        return f"({left} {self.op} {right})"

    def __eq__(self, other: object) -> bool:
        """Also needed for using gates as dict-keys."""
        if not isinstance(other, Gate):
            return NotImplemented
        return self.inputs == other.inputs and self.op == other.op

    def __hash__(self) -> int:
        """For using gates as dict-keys."""
        return hash((self.inputs, self.op))


type GateState = dict[Wire, Gate]


def parse2(text: str) -> dict[Wire, Gate]:
    _, gates = text.split("\n\n")
    gate_dict = {}

    for line in gates.split("\n"):
        w1, op, w2, _, w3 = line.split(" ")
        gate_dict[w3] = Gate(w1, op, w2)
    return gate_dict


GATE_STATE: dict[Wire, Gate] = parse2(data)
WIRE_BY_GATE: dict[Gate, Wire] = {g: w for w, g in GATE_STATE.items()}


def wire_str(w: str, i: int) -> str:
    """Write appropriate string (with optional leading zero) for wire."""
    return w + str(i).zfill(2)


def recursive_str(wire: Wire) -> str:
    # Helper function for print_gate
    if (gate := GATE_STATE.get(wire)) is None:
        return wire
    left, right = tuple(gate.inputs)
    return f"({wire}: {recursive_str(left)} {gate.op} {recursive_str(right)})"


def print_gate(wire: Wire) -> None:
    print(recursive_str(wire))


def find(op: Command, w1: Wire, w2: Wire) -> Wire:
    gate = Gate(w1, op, w2)
    # If this returns key-error, try swapping some wires ;)
    return WIRE_BY_GATE[gate]


def swap_wires(w1: Wire, w2: Wire) -> None:
    print(f"Swapping {w1} and {w2}")
    tmp = GATE_STATE[w1]
    GATE_STATE[w1] = GATE_STATE[w2]
    GATE_STATE[w2] = tmp
    WIRE_BY_GATE[GATE_STATE[w1]] = w1
    WIRE_BY_GATE[GATE_STATE[w2]] = w2


def find_zi(i: int, r_prev: Wire) -> tuple[Wire, Wire]:
    wxor = find("XOR", wire_str("x", i), wire_str("y", i))
    z = find("XOR", wxor, r_prev)
    return z, wxor


def find_ri(i: int, r_prev: Wire) -> Wire:
    wand = find("AND", wire_str("x", i), wire_str("y", i))
    wxor = find("XOR", wire_str("x", i), wire_str("y", i))
    tmp = find("AND", wxor, r_prev)
    return find("OR", wand, tmp)


z0 = find("XOR", "x00", "y00")
r0 = find("AND", "x00", "y00")

r = r0
wxor = z0
swap_wires("z09", "hnd")
swap_wires("z16", "tdv")
swap_wires("z23", "bks")
swap_wires("tjp", "nrn")  # Last one done by trial and error

# If no key-errors, then this works as it is supposed to
for i in range(1, 45):
    z, wxor = find_zi(i, r)
    z_gate = GATE_STATE[z]
    if z != wire_str("z", i):
        print(f"{wire_str("z", i)}: {z}")
        print(f"{wire_str("z", i)}: {z}, {z_gate.inputs}")
        print(f"\t{wire_str("r", i)}: {r}")
        print(f"\t{wire_str("xor", i)}: {wxor}")
        break
    if z_gate.inputs != {r, wxor}:
        print(f"{wire_str("z", i)}: {z}, {z_gate.inputs}")
        print(f"\t{wire_str("r", i)}: {r}")
        print(f"\t{wire_str("xor", i)}: {wxor}")
        break
    r = find_ri(i, r)

# After finishing, last remainder r should be equal to z45
if r != "z45":
    print(r)
    raise ValueError

result = ",".join(
    sorted(["z09", "hnd", "z16", "tdv", "z23", "bks", "tjp", "nrn"])
)
print()
print(f"Part 2 real:\n{result}")
