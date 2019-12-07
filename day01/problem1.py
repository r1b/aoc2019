import math

print(
    sum(
        [
            math.floor(int(mass.strip()) / 3) - 2
            for mass in open("input.txt").readlines()
        ]
    )
)
