# FIXME: This is naive and has horrible polynomial complexity - optimize
# before you proceed.

import operator
from dataclasses import dataclass
from typing import Set


ASTEROID = "#"


@dataclass
class Space:
    asteroids: Set["Asteroid"]

    def __init__(self):
        self.asteroids = set([])

    @classmethod
    def parse(cls, filename):
        space = cls()
        for y, line in enumerate(open(filename).readlines()):
            for x, point in enumerate(line.strip()):
                if point == ASTEROID:
                    space.add_asteroid(Asteroid(x, y, space))
        return space

    def add_asteroid(self, asteroid):
        self.asteroids.add(asteroid)

    def get_asteroids_for_asteroid(self, asteroid):
        return self.asteroids - {asteroid}

    def get_asteroids_for_line(self, line):
        return self.asteroids - {line.src, line.dst}

    def __iter__(self):
        for asteroid in self.asteroids:
            yield asteroid


@dataclass
class LineOfSight:
    src: "Asteroid"
    dst: "Asteroid"

    @property
    def slope(self):
        try:
            return (self.src.y - self.dst.y) / (self.src.x - self.dst.x)
        except ZeroDivisionError:
            return float("inf")

    def obstructed_by(self, asteroid):
        if self.slope == float("inf"):
            obstructs = (
                (self.src.y <= asteroid.y and asteroid.y <= self.dst.y)
                or (self.src.y >= asteroid.y and asteroid.y >= self.dst.y)
            ) and asteroid.x == self.src.x
        elif self.slope == 0:
            obstructs = (
                (self.src.x <= asteroid.x and asteroid.x <= self.dst.x)
                or (self.src.x >= asteroid.x and asteroid.x >= self.dst.x)
            ) and asteroid.y == self.src.y
        else:
            obstructs = (
                (
                    (self.src.x <= asteroid.x and asteroid.x <= self.dst.x)
                    or (self.src.x >= asteroid.x and asteroid.x >= self.dst.x)
                )
                and (
                    (self.src.y <= asteroid.y and asteroid.y <= self.dst.y)
                    or (self.src.y >= asteroid.y and asteroid.y >= self.dst.y)
                )
                and (
                    (asteroid.y - self.dst.y)
                    == (self.slope * (asteroid.x - self.dst.x))
                )
            )

        if obstructs:
            print(f"{self} obstructed by {asteroid}")

        return obstructs

    def __str__(self):
        return f"{self.src} -> {self.dst} m={self.slope}"


@dataclass
class Asteroid:
    x: int
    y: int
    space: Space

    def __gt__(self, other):
        return len(self) > len(other)

    def __len__(self):
        return len(
            [
                line
                for line in (
                    LineOfSight(self, asteroid)
                    for asteroid in self.space.get_asteroids_for_asteroid(self)
                )
                if not any(
                    line.obstructed_by(asteroid)
                    for asteroid in self.space.get_asteroids_for_line(line)
                )
            ]
        )

    def __hash__(self):
        return hash((self.x, self.y))

    def __str__(self):
        return f"{self.x}, {self.y}"


if __name__ == "__main__":
    print(len(max(Space.parse("input.txt"))))
