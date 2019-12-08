from dataclasses import dataclass
from enum import IntEnum


class Opcode(IntEnum):
    ADD = 1
    MUL = 2
    STORE = 3
    LOAD = 4
    HALT = 99

    @classmethod
    def parse(cls, raw_opcode):
        return int(value.lstrip('0'))



class Mode(IntEnum):
    POSITION = 0
    IMMEDIATE = 1

    @classmethod
    def parse(cls, value):
        return int(value)

@dataclass
class Parameter:
    mode: Mode
    value: Optional[int]


@dataclass
class Instruction:
    opcode: Opcode
    parameters: [Parameter]
    @classmethod
    def parse(cls, value):
        pass

    def __len__(self):
        return len(self.parameters) + 1


def parse_instruction(program, ip):
    value = str(program[ip])
    opcode, parameter_modes = Opcode.parse(value[-2:]), [Mode.parse(raw_mode) for raw_mode in value[:-2][::-1]]

def exec_program(program):
    ip = 0

    while True:
        instruction = parse_instruction(program, ip)
        ip = exec_instruction(program, ip, instruction)

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
