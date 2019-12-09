from dataclasses import dataclass


# FIXME: Can't make a dataclass with a member that is of the same type?
class SpaceObject:
    def __init__(self, name, orbits=None):
        self.name = name
        self.orbits = orbits

    def num_orbits(self):
        return 0 if self.orbits is None else 1 + self.orbits.num_orbits()


# LOL I think this is backwards but it still works??
@dataclass
class Orbit:
    parent_name: str
    child_name: str

    @classmethod
    def parse(cls, raw_orbit):
        return cls(*raw_orbit.strip().split(")"))


def count_orbits(filename):
    space_objects = {}

    for orbit in (Orbit.parse(line) for line in open(filename).readlines()):
        if orbit.parent_name not in space_objects:
            space_objects[orbit.parent_name] = SpaceObject(orbit.parent_name)

        if orbit.child_name not in space_objects:
            space_objects[orbit.child_name] = SpaceObject(
                orbit.child_name, space_objects[orbit.parent_name]
            )
        else:
            space_objects[orbit.child_name].orbits = space_objects[orbit.parent_name]

    return sum(space_object.num_orbits() for space_object in space_objects.values())


print(count_orbits("input.txt"))
