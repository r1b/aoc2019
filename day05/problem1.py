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
        return int(raw_opcode.lstrip("0"))


OPCODE_PARAMETER_COUNT = {
    Opcode.ADD: 3,
    Opcode.MUL: 3,
    Opcode.STORE: 1,
    Opcode.LOAD: 1,
    Opcode.HALT: 0,
}


class Mode(IntEnum):
    POSITION = 0
    IMMEDIATE = 1

    @classmethod
    def parse(cls, raw_mode):
        return int(raw_mode)


@dataclass
class Parameter:
    mode: Mode
    value: int

    def get_value(self, program, writable=False):
        if writable or self.mode == Mode.IMMEDIATE:
            return self.value
        else:
            return program.read_memory(self.value)

    def __repr__(self):
        return f"Parameter(mode={Mode(self.mode).name}, value={self.value})"


@dataclass
class Instruction:
    opcode: Opcode
    parameters: [Parameter]

    @classmethod
    def parse(cls, program):
        raw_instruction = str(program.read_memory(program.ip))
        opcode = Opcode.parse(raw_instruction[-2:])

        parameter_modes = [Mode.POSITION] * OPCODE_PARAMETER_COUNT[opcode]
        for i, raw_mode in enumerate(raw_instruction[:-2][::-1]):
            parameter_modes[i] = Mode.parse(raw_mode)

        instruction = cls(
            opcode,
            [
                Parameter(mode, program.read_memory(program.ip + i + 1))
                for i, mode in enumerate(parameter_modes)
            ],
        )

        print(instruction)

        return instruction

    def execute(self, program):
        if self.opcode == Opcode.ADD:
            program.write_memory(
                self.parameters[2].get_value(program, writable=True),
                self.parameters[0].get_value(program)
                + self.parameters[1].get_value(program),
            )
        elif self.opcode == Opcode.MUL:
            program.write_memory(
                self.parameters[2].get_value(program, writable=True),
                self.parameters[0].get_value(program)
                * self.parameters[1].get_value(program),
            )
        elif self.opcode == Opcode.STORE:
            address = self.parameters[0].get_value(program, writable=True)
            value = int(input(f"Input value for address={address}: "))
            program.write_memory(
                address, value,
            )
        elif self.opcode == Opcode.LOAD:
            value = self.parameters[0].get_value(program)
            print(f"Output value: {value}")
        elif self.opcode == Opcode.HALT:
            raise StopIteration()
        else:
            raise ValueError(f"Invalid opcode={self.opcode}")

        program.step(len(self))

    def __len__(self):
        return OPCODE_PARAMETER_COUNT[self.opcode] + 1

    def __str__(self):
        return f"Instruction(opcode={Opcode(self.opcode).name} parameters={self.parameters} size={len(self)})"


@dataclass(init=False)
class Program:
    memory: [int]
    ip: int

    def __init__(self, memory, ip=0):
        self.memory = memory
        self.ip = ip

    @property
    def result(self):
        return self.memory[0]

    def read_memory(self, address):
        return self.memory[address]

    def write_memory(self, address, value):
        print(f"Wrote {value} to {address}")
        self.memory[address] = value

    def step(self, num_values):
        self.ip += num_values

    @classmethod
    def parse(cls, filename):
        return cls(
            [
                int(instruction)
                for instruction in open(filename).readline().strip().split(",")
            ]
        )

    @classmethod
    def execute(cls, filename):
        program = cls.parse(filename)

        while True:
            instruction = Instruction.parse(program)
            try:
                instruction.execute(program)
            except StopIteration:
                break

        return program.result


Program.execute("input.txt")
