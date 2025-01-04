from __future__ import annotations

from enum import Enum, auto
from functools import cache, partial

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
    """Store non-recursive data structure in Tree.

    Do it like this, and store them in a dict, so we can easily update one gate.
    """

    def __init__(self, left: Wire, op: Command, right: Wire) -> None:
        """Pass nothing."""
        # self.left = left
        self.op = op
        # self.right = right
        if left == right:
            raise ValueError
        self.inputs = frozenset({left, right})

    def __str__(self) -> str:
        # return f"({self.name}: {self.left!s} {self.op} {self.right!s})"
        left, right = tuple(self.inputs)
        return f"({left} {self.op} {right})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Gate):
            return NotImplemented
        return self.inputs == other.inputs and self.op == other.op

    def __hash__(self) -> int:
        return hash((self.inputs, self.op))


type GateState = dict[Wire, Gate]


# class RecGate:
#     """Store recursive data structure in Tree."""
#
#     def __init__(
#         self,
#         name: str,
#         left: RecGate | Wire,
#         op: Command,
#         right: RecGate | Wire,
#     ) -> None:
#         self.name = name
#         self.left = left
#         self.op = op
#         self.right = right
#
#     def __str__(self) -> str:
#         left = self.left.name if self.left is RecGate else self.left
#         right = self.right.name if self.right is RecGate else self.right
#         return f"({left} {self.op} {right})"
#
#     def rec_print(self) -> str:
#         left = self.left.rec_print() if self.left is RecGate else self.left
#         right = self.right.rec_print() if self.right is RecGate else self.right
#         return f"({left} {self.op} {right})"
#
#     def check_val(self) -> int:
#         """Compute comparison-value for recursive gate.
#
#         Builds on assumption that whenever x_i and y_j is compared, then i =
#         j. Instantiate all x_i's with 011 and all y_i's with 001. (neither 1,
#         one 1, both 1, all commands are also symmetrix, so don't need to
#         distinguish whether x or y is 1.
#         """
#         return do_command(
#             self.op, self.left.check_val(), self.right.check_val()
#         )


test3 = """\
x00: 0
x01: 1
x02: 0
x03: 1
x04: 0
x05: 1
y00: 0
y01: 0
y02: 1
y03: 1
y04: 0
y05: 1

x00 AND y00 -> z05
x01 AND y01 -> z02
x02 AND y02 -> z01
x03 AND y03 -> z03
x04 AND y04 -> z04
x05 AND y05 -> z00\
"""


def parse2(text: str) -> GateState:
    _, gates = text.split("\n\n")
    gate_dict = {}

    for line in gates.split("\n"):
        w1, logic, w2, _, w3 = line.split(" ")
        gate_dict[w3] = Gate(w1, logic, w2)
    return gate_dict


def wire_str(w: str, i: int) -> str:
    return w + str(i).zfill(2)


DEFAULT_WIRES = {wire_str(c, i) for i in range(45) for c in ["x", "y"]}


def recursive_str(gate_state: GateState, wire: Wire) -> str:
    if wire not in gate_state:
        return wire
    fun = partial(recursive_str, gate_state)
    gate = gate_state[wire]
    left, right = tuple(gate.inputs)
    return f"({wire}: {fun(left)} {gate.op} {fun(right)})"


def print_gate(gate_state: GateState, wire: Wire) -> None:
    print(recursive_str(gate_state, wire))


def check_val(gate_state: GateState, on: dict[Wire, int], wire: Wire) -> int:
    # Give some wires a specified binary value for testing
    if wire in on:
        return on[wire]
    # Nooo, bad idea, what if any random ones started with this...
    # if wire.startswith(("x", "y")):
    if wire in DEFAULT_WIRES:
        return 0
    gate = gate_state[wire]
    fun = partial(check_val, gate_state, on)
    left, right = tuple(gate.inputs)
    return do_command(gate.op, fun(left), fun(right))


# Global variable now
GATE_STATE = parse2(data)
WIRE_BY_GATE = {g: w for w, g in GATE_STATE.items()}


def find(op: Command, w1: Wire, w2: Wire) -> Wire:
    gate = Gate(w1, op, w2)
    # return WIRE_BY_GATE.get(gate)
    return WIRE_BY_GATE[gate]
    # for w, g in GATE_STATE.items():
    #     if g == gate:
    #         return w
    # raise ValueError


def swap_wires(w1: Wire, w2: Wire) -> None:
    print(f"Swapping {w1} and {w2}")
    tmp = GATE_STATE[w1]
    GATE_STATE[w1] = GATE_STATE[w2]
    GATE_STATE[w2] = tmp
    WIRE_BY_GATE[GATE_STATE[w1]] = w1
    WIRE_BY_GATE[GATE_STATE[w2]] = w2


# Lists of primitive wires
# XORS = []
# ANDS = []
# # ONLY TO TEST THAT EACH ONE DOES OCCUR PRECISELY ONCE!
# for i in range(45):
#     xors = [
#         w
#         for w, g in GATE_STATE.items()
#         if {g.left, g.right} == {wire_str("x", i), wire_str("y", i)}
#         and g.op == "XOR"
#     ]
#     if len(xors) != 1:
#         XORS.append(xors[0])
#     else:
#         raise ValueError
#
# for i in range(45):
#     ands = [
#         w
#         for w, g in GATE_STATE.items()
#         if {g.left, g.right} == {wire_str("x", i), wire_str("y", i)}
#         and g.op == "AND"
#     ]
#     if len(ands) == 1:
#         ANDS.append(ands[0])
#     else:
#         raise ValueError


CORRECT_GATE_STATE: GateState = {}
CORRECT_GATE_STATE.update(
    {
        wire_str("xor", i): Gate(wire_str("x", i), "XOR", wire_str("y", i))
        for i in range(45)
    }
)
CORRECT_GATE_STATE.update(
    {
        wire_str("and", i): Gate(wire_str("x", i), "AND", wire_str("y", i))
        for i in range(45)
    }
)


def add_remainder(i: int) -> None:
    if i == 0:
        gate = CORRECT_GATE_STATE["and00"]
        CORRECT_GATE_STATE[wire_str("r", i)] = gate
    else:
        tmp_gate = Gate(wire_str("xor", i), "AND", wire_str("r", i - 1))
        # "t" for "temporary"
        tmp_wire = wire_str("tmp", i)
        CORRECT_GATE_STATE[tmp_wire] = tmp_gate
        gate = Gate(wire_str("and", i), "OR", tmp_wire)
    CORRECT_GATE_STATE[wire_str("r", i)] = gate


def add_z(i: int) -> None:
    if i == 0:
        gate = CORRECT_GATE_STATE["xor00"]
    else:
        gate = Gate(wire_str("xor", i), "XOR", wire_str("r", i - 1))
    CORRECT_GATE_STATE[wire_str("z", i)] = gate


for i in range(45):
    add_z(i)
    add_remainder(i)
# add_remainder(45)
# CORRECT_GATE_STATE["z45"] = CORRECT_GATE_STATE.pop("r45")
# Don't do that like this -- z45 is different, as it can only come as remainder!
# add_z(45)


def checker_remainder(i: int) -> dict[Wire, int]:
    return {
        wire_str("r", i - 1): 0b10,
        wire_str("x", i): 0b11,
        wire_str("y", i): 0b01,
        wire_str("y", i + 1): 0b10,
    }


def xor_valid(i: int, wire: Wire) -> bool:
    on = {
        wire_str("x", i): 0b0101010101010101,
        wire_str("y", i): 0b0011001100110011,
        wire_str("x", i - 1): 0b0000111100001111,
        wire_str("y", i - 1): 0b0000000011111111,
    }
    return check_val(GATE_STATE, on, wire) == 0b0110011001100110


def remainder_valid(i: int, wire: Wire) -> bool:
    on = {
        wire_str("x", i): 0b011011011011,
        wire_str("y", i): 0b001001001001,
        wire_str("x", i - 1): 0b000111000111,
        wire_str("y", i - 1): 0b000111000111,
        wire_str("x", i + 1): 0b000000111111,
    }

    # expected = (on[wire_str("x", i)] & on[wire_str("y", i)]) | (
    #     (on[wire_str("x", i)] ^ on[wire_str("y", i)])
    #     & (on[wire_str("x", i - 1)] & on[wire_str("y", i - 1)])
    # )
    expected = 0b001011001011
    expected_i_zero = 0b001001001001

    return check_val(GATE_STATE, on, wire) == (
        expected_i_zero if i == 0 else expected
    )


# for i in range(45):
#     print({x for x in GATE_STATE if remainder_valid(i, x)})

# print({x for x in GATE_STATE if remainder_valid(1, x)})


class WireError(Enum):  # noqa: D101
    Z_ERROR = auto()
    XOR_ERROR = auto()
    REMAINDER_ERROR = auto()
    OH_NO = auto()
    OK = auto()


def z_valid(i: int) -> tuple[WireError, Wire]:
    wire = wire_str("z", i)
    gate = GATE_STATE[wire]
    if gate.op != "XOR":
        return WireError.Z_ERROR, wire
    if i == 0:
        if xor_valid(0, wire):
            return WireError.OK, ""
        return WireError.OH_NO, ""
    if not any(xor_valid(i, w) for w in gate.inputs):
        return WireError.XOR_ERROR, ""
    if any(remainder_valid(i - 1, w) for w in gate.inputs):
        return WireError.OK, ""
    return WireError.REMAINDER_ERROR, ""


test = Gate("x07", "XOR", "y07")
z0 = find("XOR", "x00", "y00")
r0 = find("AND", "x00", "y00")


def find_zi(i: int, r_prev: Wire) -> tuple[Wire, Wire]:
    wxor = find("XOR", wire_str("x", i), wire_str("y", i))
    z = find("XOR", wxor, r_prev)
    return z, wxor


def find_ri(i: int, r_prev: Wire) -> Wire:
    wand = find("AND", wire_str("x", i), wire_str("y", i))
    wxor = find("XOR", wire_str("x", i), wire_str("y", i))
    tmp = find("AND", wxor, r_prev)
    return find("OR", wand, tmp)


r = r0
wxor = z0
swap_wires("z09", "hnd")
swap_wires("z16", "tdv")
swap_wires("z23", "bks")
swap_wires("tjp", "nrn")  # Last one by trial and error, xd

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

print(
    ",".join(sorted(["z09", "hnd", "z16", "tdv", "z23", "bks", "tjp", "nrn"]))
)
