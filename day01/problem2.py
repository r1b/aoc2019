import math


def compute_fuel(v):
    return math.floor(v / 3) - 2


total_fuel = 0

for line in open("input.txt").readlines():
    fuel = compute_fuel(int(line.strip()))
    while True:
        total_fuel += fuel
        next_fuel = compute_fuel(fuel)
        if next_fuel <= 0:
            break
        fuel = next_fuel

print(total_fuel)
