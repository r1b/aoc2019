from dataclasses import dataclass
from enum import IntEnum
from itertools import permutations


MEMORY_SIZE = 4096


class Opcode(IntEnum):
    ADD = 1
    MUL = 2
    STORE = 3
    LOAD = 4
    JUMP_IF_TRUE = 5
    JUMP_IF_FALSE = 6
    LESS_THAN = 7
    EQUALS = 8
    ADJUST_RELATIVE_BASE = 9
    HALT = 99

    @classmethod
    def parse(cls, raw_opcode):
        return int(raw_opcode.lstrip("0"))


OPCODE_PARAMETER_COUNT = {
    Opcode.ADD: 3,
    Opcode.MUL: 3,
    Opcode.STORE: 1,
    Opcode.LOAD: 1,
    Opcode.JUMP_IF_TRUE: 2,
    Opcode.JUMP_IF_FALSE: 2,
    Opcode.LESS_THAN: 3,
    Opcode.EQUALS: 3,
    Opcode.ADJUST_RELATIVE_BASE: 1,
    Opcode.HALT: 0,
}


class Mode(IntEnum):
    POSITION = 0
    IMMEDIATE = 1
    RELATIVE = 2

    @classmethod
    def parse(cls, raw_mode):
        return int(raw_mode)


@dataclass
class Parameter:
    mode: Mode
    value: int

    def get_value(self, program, writable=False):
        if self.mode == Mode.IMMEDIATE:
            return self.value
        elif self.mode == Mode.RELATIVE:
            if writable:
                return program.relative_base + self.value
            else:
                return program.read_memory(program.relative_base + self.value)
        else:
            if writable:
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

        return instruction

    def execute(self, program):
        result = None
        wrote_ip = False

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
            value = program.inputs.pop(0)
            program.write_memory(
                address, value,
            )
        elif self.opcode == Opcode.LOAD:
            result = self.parameters[0].get_value(program)
        elif self.opcode == Opcode.JUMP_IF_TRUE:
            test = self.parameters[0].get_value(program)
            address = self.parameters[1].get_value(program)
            if test != 0:
                program.jump(address)
                wrote_ip = True
        elif self.opcode == Opcode.JUMP_IF_FALSE:
            test = self.parameters[0].get_value(program)
            address = self.parameters[1].get_value(program)
            if test == 0:
                program.jump(address)
                wrote_ip = True
        elif self.opcode == Opcode.LESS_THAN:
            value = (
                1
                if (
                    self.parameters[0].get_value(program)
                    < self.parameters[1].get_value(program)
                )
                else 0
            )
            program.write_memory(
                self.parameters[2].get_value(program, writable=True), value
            )
        elif self.opcode == Opcode.EQUALS:
            value = (
                1
                if (
                    self.parameters[0].get_value(program)
                    == self.parameters[1].get_value(program)
                )
                else 0
            )
            program.write_memory(
                self.parameters[2].get_value(program, writable=True), value
            )
        elif self.opcode == Opcode.ADJUST_RELATIVE_BASE:
            offset = self.parameters[0].get_value(program)
            program.adjust_relative_base(offset)
        elif self.opcode == Opcode.HALT:
            raise StopIteration()
        else:
            raise ValueError(f"Invalid opcode={self.opcode}")

        if not wrote_ip:
            program.step(len(self))

        return result

    def __len__(self):
        return OPCODE_PARAMETER_COUNT[self.opcode] + 1

    def __str__(self):
        return f"Instruction(opcode={Opcode(self.opcode).name} parameters={self.parameters} size={len(self)})"


@dataclass(init=False)
class Program:
    memory: [int]
    ip: int

    def __init__(self, memory, ip=0, relative_base=0, inputs=None):
        self.memory = memory + [0] * MEMORY_SIZE
        self.ip = ip
        self.relative_base = relative_base
        self.inputs = inputs or []

    @classmethod
    def parse(cls, filename, inputs=None):
        return cls(
            [
                int(instruction)
                for instruction in open(filename).readline().strip().split(",")
            ],
            inputs=inputs,
        )

    @property
    def result(self):
        return self.memory[0]

    def read_memory(self, address):
        return self.memory[address]

    def write_memory(self, address, value):
        self.memory[address] = value

    def step(self, num_values):
        self.ip += num_values

    def jump(self, address):
        self.ip = address

    def adjust_relative_base(self, offset):
        self.relative_base += offset

    def add_input(self, value):
        self.inputs.append(value)

    def __iter__(self):
        return self

    def __next__(self):
        while True:
            instruction = Instruction.parse(self)
            result = instruction.execute(self)
            if result is not None:
                return result


program = Program.parse("input.txt", [2])
print(next(program))
