from functools import cache, partial
from typing import Any, cast
import pyparsing as pp

from aocd import get_data

from enum import Enum


class Instruction(Enum):
    """Convert opcode to instruction."""

    adv = 0
    bxl = 1
    bst = 2
    jnz = 3
    bxc = 4
    out = 5
    bdv = 6
    cdv = 7


class Register(Enum):
    """Convert combo operands to regisers."""

    A = 4
    B = 5
    C = 6


type Operand = int
type Command = tuple[Instruction, Operand]
type RegisterState = dict[Register, int]

# Data
data = get_data(year=2024, day=17)

test = """\
Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0"""

test2 = """\
Register A: 0
Register B: 0
Register C: 9

Program: 2,6"""

test3 = """\
Register A: 10
Register B: 0
Register C: 0

Program: 5,0,5,1,5,4"""

test4 = """\
Register A: 2024
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0"""

test5 = """\
Register A: 0
Register B: 29
Register C: 0

Program: 1,7"""

test6 = """\
Register A: 0
Register B: 2024
Register C: 43690

Program: 4,0"""


# Convert data (text) to workable input
def parse(text: str) -> tuple[RegisterState, list[Command]]:
    register = pp.Suppress("Register" + pp.Char("ABC") + ":") + pp.common.number
    program = pp.Suppress("Program:") + pp.DelimitedList(pp.common.number)
    split = text.split("\n\n")
    register_dict = dict(
        zip(
            [Register.A, Register.B, Register.C],
            (register * 3).parse_string(split[0]).as_list(),
        )
    )
    program_list = program.parse_string(split[1]).as_list()
    instructions = [Instruction(x) for x in program_list[::2]]
    operands = program_list[1::2]
    commands = list(zip(instructions, operands))

    return (register_dict, commands)


def combo_operand(registers: RegisterState, operand: Operand) -> int:
    match operand:
        case 0 | 1 | 2 | 3:
            return operand
        case 4 | 5 | 6:
            return registers[Register(operand)]
        case _:
            raise ValueError


def adv(registers: RegisterState, operand: Operand) -> None:
    res = registers[Register.A] // (2 ** combo_operand(registers, operand))
    registers[Register.A] = res


def bxl(registers: RegisterState, operand: Operand) -> None:
    res = registers[Register.B] ^ operand
    registers[Register.B] = res


def bst(registers: RegisterState, operand: Operand) -> None:
    registers[Register.B] = combo_operand(registers, operand) % 8


def jnz(registers: RegisterState, operand: Operand) -> int:
    # Assumes that operand is always even. Output is index to jump to
    if registers[Register.A] == 0:
        return -1  # -1 indicates no jump
    if operand % 2 == 1:
        raise ValueError
    return operand // 2


def bxc(registers: RegisterState) -> None:
    # Still skips over operand, but doesn't use it
    res = registers[Register.B] ^ registers[Register.C]
    registers[Register.B] = res


def out(registers: RegisterState, operand: Operand) -> int:
    return combo_operand(registers, operand) % 8


def bdv(registers: RegisterState, operand: Operand) -> None:
    res = registers[Register.A] // (2 ** combo_operand(registers, operand))
    registers[Register.B] = res


def cdv(registers: RegisterState, operand: Operand) -> None:
    res = registers[Register.A] // (2 ** combo_operand(registers, operand))
    registers[Register.C] = res


def execute(
    registers: dict[Register, int],
    output: list[int],
    command: Command,
    pointer: int,
) -> int:
    instruction, operand = command
    instruction = Instruction(instruction)
    match instruction:
        case Instruction.adv:
            adv(registers, operand)
        case Instruction.bxl:
            bxl(registers, operand)
        case Instruction.bst:
            bst(registers, operand)
        case Instruction.jnz:
            return jnz(registers, operand)
        case Instruction.bxc:
            bxc(registers)
        case Instruction.out:
            output.append(out(registers, operand))
        case Instruction.bdv:
            bdv(registers, operand)
        case Instruction.cdv:
            cdv(registers, operand)
    return pointer + 1


def part1(text: str) -> str:
    registers, commands = parse(text)
    output: list[int] = []
    execute_with_state = partial(execute, registers, output)
    pointer = 0
    while pointer != -1 and pointer < len(commands):
        pointer = execute_with_state(commands[pointer], pointer)
    # print(registers)
    return ",".join(str(x) for x in output)


print("Part 1 test:", part1(test))
# print("Part 1 test2:", part1(test2))
# print("Part 1 test3:", part1(test3))
# print("Part 1 test4:", part1(test4))
# print("Part 1 test5:", part1(test5))
# print("Part 1 test6:", part1(test6))
print("Part 1 real:", part1(data))


# Part 2

testpt2 = """\
Register A: 2024
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0
"""


@cache
def hashable_output(
    A: int, B: int, C: int, commands: list[Command]
) -> tuple[int, int, int]:
    registers = {Register.A: A, Register.B: B, Register.C: C}
    pointer = 0
    output = []
    while pointer != -1:
        pointer = execute(registers, output, commands[pointer], pointer)
    return (registers[Register.A], registers[Register.B], registers[Register.C])


def execute_v2(
    registers: dict[Register, int],
    output: list[int],
    correct_output: list[int],
    command: Command,
    pointer: int,
) -> int:
    # Abort if out returns something wrong
    instruction, operand = command
    instruction = Instruction(instruction)
    match instruction:
        case Instruction.adv:
            adv(registers, operand)
        case Instruction.bxl:
            bxl(registers, operand)
        case Instruction.bst:
            bst(registers, operand)
        case Instruction.jnz:
            return jnz(registers, operand)
        case Instruction.bxc:
            bxc(registers)
        case Instruction.out:
            output_val = out(registers, operand)
            output_index = len(output)
            if (
                output_index >= len(correct_output)
                or correct_output[output_index] != output_val
            ):
                return -1
            output.append(out(registers, operand))
        case Instruction.bdv:
            bdv(registers, operand)
        case Instruction.cdv:
            cdv(registers, operand)
    return pointer + 1


def output(
    registers: RegisterState, commands: list[Command], correct_output: list[int]
) -> list[int]:
    registers = registers.copy()  # Don't mutate registers
    output: list[int] = []
    execute_with_state = partial(execute_v2, registers, output, correct_output)
    pointer = 0
    i = 0
    while pointer != -1 and pointer < len(commands):
        i += 1
        pointer = execute_with_state(commands[pointer], pointer)
    # return ",".join(str(x) for x in output)
    return output


def part2(text: str) -> int:
    return 0
    # registers, commands = parse(text)
    # program = pp.Suppress("Program:") + pp.Word(pp.nums + ",")
    # vals = program.parse_string(text.split("\n\n")[1])
    # # correct_output = program.parse_string(text.split("\n\n")[1])[0]
    # # print(vals[0])
    # correct_output = [int(x) for x in (vals[0]).split(",")]
    # # print(correct_output)
    # i = 0
    # # print(output(registers, commands, correct_output))
    # # registers[Register.A] = 117440
    # # print(output(registers, commands, correct_output))
    # while output(registers, commands, correct_output) != correct_output:
    #     i += 1
    #     if i & 65535 == 0:
    #         print(str(i) + "\r", end="")
    #     registers[Register.A] = i
    # print("Done", " " * 30)
    # return i


# New idea: It seems the program is made such that the last step is always jump
# to the start, and the penultimate step is reading from some register.
# So we need to find the inverse of all commands, and run it backwards, once for
# each value to be printed.
# Output we want is Program:
# 2,4,
# 1,5,
# 7,5,
# 1,6,
# 0,3,
# 4,6,
# 5,5,
# 3,0. (8 commands, 6
# computational commands)
# We must start (from behind) with A = 0, and then we must have that A neq 0 on
# each subsequent pass

test_reg = {Register.A: 1010, Register.B: 0, Register.C: 0}

program = pp.Suppress("Program:") + pp.DelimitedList(pp.common.number)
split = data.split("\n\n")
# register_dict = dict(
#     zip(
#         [Register.A, Register.B, Register.C],
#         (register * 3).parse_string(split[0]).as_list(),
#     )
# )
program_list = program.parse_string(split[1]).as_list()
instructions = [Instruction(x) for x in program_list[::2]]
operands = program_list[1::2]
commands = list(zip(instructions, operands))


def print_register(register: RegisterState) -> None:
    print("Register A:", register[Register.A])
    print("Register B:", register[Register.B])
    print("Register C:", register[Register.C])
    print()


vals: list[int] = []
execute_with_state = partial(execute, test_reg, vals)
pointer = 0
for _ in range(10):
    print(commands[pointer])
    pointer = execute_with_state(commands[pointer], pointer)
    print_register(test_reg)

# print("Part 2 test:", part2(testpt2))
# print("Part 2 real:", part2(data))
# Checked manually up to about 650000 :/
# now up to 291897344
