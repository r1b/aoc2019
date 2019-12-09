from dataclasses import dataclass


# FIXME: Can't make a dataclass with a member that is of the same type?
class SpaceObject:
    def __init__(self, name, orbits_object=None, orbited_by_objects=None):
        self.name = name
        self.orbits_object = orbits_object
        self.orbited_by_objects = orbited_by_objects or set([])

    def __hash__(self):
        return hash(self.name)


@dataclass
class Orbit:
    child_name: str
    parent_name: str

    @classmethod
    def parse(cls, raw_orbit):
        return cls(*raw_orbit.strip().split(")"))


@dataclass
class TransferPath:
    space_object: SpaceObject
    steps: int


def find_santa(filename):
    space_objects = {}
    seen_objects = set([])
    next_paths = []

    for orbit in (Orbit.parse(line) for line in open(filename).readlines()):
        if orbit.parent_name not in space_objects:
            space_objects[orbit.parent_name] = SpaceObject(orbit.parent_name)

        if orbit.child_name not in space_objects:
            space_objects[orbit.child_name] = SpaceObject(orbit.child_name)

        space_objects[orbit.parent_name].orbits_object = space_objects[orbit.child_name]
        space_objects[orbit.child_name].orbited_by_objects.add(
            space_objects[orbit.parent_name]
        )

    cur = space_objects["YOU"]
    seen_objects.add(cur)

    if cur.orbits_object is not None:
        next_paths.append(TransferPath(cur.orbits_object, 0))
    if len(cur.orbited_by_objects) > 0:
        for space_object in cur.orbited_by_objects:
            next_paths.append(TransferPath(space_object, 0))

    while True:
        cur_path = next_paths.pop()
        cur = cur_path.space_object
        print(f"Visited {cur.name}")
        seen_objects.add(cur)

        if cur.orbits_object is not None:
            if cur.orbits_object not in seen_objects:
                next_paths.append(TransferPath(cur.orbits_object, cur_path.steps + 1))
        if len(cur.orbited_by_objects) > 0:
            for space_object in cur.orbited_by_objects:
                if space_object.name == "SAN":
                    return cur_path.steps
                if space_object not in seen_objects:
                    next_paths.append(TransferPath(space_object, cur_path.steps + 1))


print(find_santa("input.txt"))
