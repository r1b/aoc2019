from collections import defaultdict
from dataclasses import dataclass


@dataclass
class WireSquare:
    x: int
    y: int

    def __hash__(self):
        return hash((self.x, self.y))


class Wire:
    def __init__(self, components):
        self.components = components
        self.cur = [0, 0]
        self.square_steps = defaultdict(dict)
        self.steps = 0
        self.visited = set([])

    @classmethod
    def parse(cls, filename):
        for line in open(filename).readlines():
            yield Wire(line.split(","))

    def __iter__(self):
        return self

    def __next__(self):
        component = self.components.pop(0)
        direction = component[0]
        distance = int(component[1:])

        if direction == "L":
            for x in range(self.cur[0] - 1, self.cur[0] - distance - 1, -1):
                self.steps += 1
                self.visited.add(WireSquare(x, self.cur[1]))
                if self.cur[1] not in self.square_steps[x]:
                    self.square_steps[x][self.cur[1]] = self.steps
            self.cur[0] = self.cur[0] - distance
        elif direction == "R":
            for x in range(self.cur[0] + 1, self.cur[0] + distance + 1):
                self.steps += 1
                self.visited.add(WireSquare(x, self.cur[1]))
                if self.cur[1] not in self.square_steps[x]:
                    self.square_steps[x][self.cur[1]] = self.steps
            self.cur[0] = self.cur[0] + distance
        elif direction == "U":
            for y in range(self.cur[1] + 1, self.cur[1] + distance + 1):
                self.steps += 1
                self.visited.add(WireSquare(self.cur[0], y))
                if y not in self.square_steps[self.cur[0]]:
                    self.square_steps[self.cur[0]][y] = self.steps
            self.cur[1] = self.cur[1] + distance
        elif direction == "D":
            for y in range(self.cur[1] - 1, self.cur[1] - distance - 1, -1):
                self.steps += 1
                self.visited.add(WireSquare(self.cur[0], y))
                if y not in self.square_steps[self.cur[0]]:
                    self.square_steps[self.cur[0]][y] = self.steps
            self.cur[1] = self.cur[1] - distance
        else:
            raise ValueError("invalid direction", direction)

        return self

    def __and__(self, other):
        ixs = self.visited & other.visited
        if ixs:
            for ix in ixs:
                yield self.square_steps[ix.x][ix.y] + other.square_steps[ix.x][ix.y]

    def __len__(self):
        return self.steps

    def __str__(self):
        return f"Wire(cur={self.cur}, steps={self.steps})"


def find_fastest_intersection():
    wires = Wire.parse("input.txt")

    wire1 = next(wires)
    wire2 = next(wires)

    while True:
        wire1 = next(wire1)
        wire2 = next(wire2)

        print("wire1", wire1)
        print("wire2", wire2)

        try:
            return next(wire1 & wire2)
        except StopIteration:
            continue


print(find_fastest_intersection())
