from enum import IntEnum


class Opcode(IntEnum):
    ADD = 1
    MUL = 2
    HALT = 99


def run_program(program):
    ip = 0

    while True:
        opcode = program[ip]

        if opcode == Opcode.ADD:
            program[program[ip + 3]] = (
                program[program[ip + 1]] + program[program[ip + 2]]
            )
        elif opcode == Opcode.MUL:
            program[program[ip + 3]] = (
                program[program[ip + 1]] * program[program[ip + 2]]
            )
        elif opcode == Opcode.HALT:
            break
        else:
            raise ValueError("You goofed", opcode)

        ip += 4

    return program[0]


def find_inputs():
    for noun in range(100):
        for verb in range(100):
            program = [
                int(instruction)
                for instruction in open("input.txt").readline().strip().split(",")
            ]

            program[1] = noun
            program[2] = verb

            result = run_program(program)

            if result == 19690720:
                return 100 * noun + verb


print(find_inputs())
