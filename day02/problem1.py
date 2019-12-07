from enum import IntEnum


class Opcode(IntEnum):
    ADD = 1
    MUL = 2
    HALT = 99


program = [
    int(instruction) for instruction in open("input.txt").readline().strip().split(",")
]

program[1] = 12
program[2] = 2

ip = 0

while True:
    opcode = program[ip]

    if opcode == Opcode.ADD:
        program[program[ip + 3]] = program[program[ip + 1]] + program[program[ip + 2]]
    elif opcode == Opcode.MUL:
        program[program[ip + 3]] = program[program[ip + 1]] * program[program[ip + 2]]
    elif opcode == Opcode.HALT:
        break
    else:
        raise ValueError("You goofed", opcode)

    ip += 4

print(program[0])
