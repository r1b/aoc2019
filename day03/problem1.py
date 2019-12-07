def parse_wire(components):
    point = [0, 0]
    points = set([])

    for component in components:
        direction = component[0]
        distance = int(component[1:])

        if direction == "L":
            for x in range(point[0] - distance, point[0] + 1):
                points.add((x, point[1]))
            point[0] = point[0] - distance
        elif direction == "R":
            for x in range(point[0], point[0] + distance + 1):
                points.add((x, point[1]))
            point[0] = point[0] + distance
        elif direction == "U":
            for y in range(point[1], point[1] + distance + 1):
                points.add((point[0], y))
            point[1] = point[1] + distance
        elif direction == "D":
            for y in range(point[1] - distance, point[1] + 1):
                points.add((point[0], y))
            point[1] = point[1] - distance
        else:
            raise ValueError("invalid direction", direction)

    return points


def find_closest_intersection():
    f = open("input.txt")

    wire1 = parse_wire(f.readline().split(","))
    wire2 = parse_wire(f.readline().split(","))

    intersections = wire1 & wire2

    return min(
        n
        for n in (sum(abs(coord) for coord in point) for point in intersections)
        if n > 0
    )


# FIXME: You could do this in O(n) but like WHATEVER
print(find_closest_intersection())
