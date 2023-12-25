from __future__ import annotations

from utils import read_file, Part
from typing import List, Tuple
import numpy as np

SCALING = 1_000_000_000


class Area:
    def __init__(self, limits: Tuple[int, int], data: List[str], part: Part):
        self.part = part
        self.limits = (limits[0], limits[1])
        self.hailstones = [Hailstone(line) for line in data]

    def get_intersections(self):
        intersections = {}
        for i in range(len(self.hailstones)):
            for j in range(i + 1, len(self.hailstones)):
                intersections[f"{i}-{j}"] = \
                    self.hailstones[i].intersect(self.hailstones[j], limits)
        return len([v for v in intersections.values() if v])

    def find_stone(self):
        # The ratio of the difference in velocities and positions must be the
        # same.  We can look at just the x-y plane and end up with an equation
        # A1 * x = b1. Then we can look at x-z plane and come up with another
        # linear equation A2 * x = b2

        a1_rows, b1_elements = [], []
        a2_rows, b2_elements = [], []
        h1 = self.hailstones[0]
        h1.x, h1.y, h1.z = h1.x / SCALING, h1.y / SCALING, h1.z / SCALING
        for i in range(1, 5):
            h2 = self.hailstones[i]
            h2.x, h2.y, h2.z = h2.x / SCALING, h2.y / SCALING, h2.z / SCALING

            a1_rows.append(h1.get_row_of_A(h2, type='x-y'))
            b1_elements.append(h1.get_element_of_b(h2, type='x-y'))

            a2_rows.append(h1.get_row_of_A(h2, type='x-z'))
            b2_elements.append(h1.get_element_of_b(h2, type='x-z'))

        # This gives us x0, y0, vx0, vy0
        A1 = np.array(a1_rows)
        b1 = np.array(b1_elements)
        xy_ans = np.linalg.solve(A1, b1)

        # This gives us x0, z0, vx0, vz0
        A2 = np.array(a2_rows)
        b2 = np.array(b2_elements)
        xz_ans = np.linalg.solve(A2, b2)

        return round(SCALING * xy_ans[0] + SCALING * xy_ans[1] + SCALING * xz_ans[1])


class Hailstone:
    def __init__(self, line: str):
        pts = line.split('@')
        self.x, self.y, self.z = tuple([int(ele) for ele in pts[0].split(',')])
        self.vx, self.vy, self.vz = tuple([int(ele) for ele in pts[1].split(',')])
        self.slope = self.vy / self.vx

    def __hash__(self):
        return hash((self.x, self.y, self.z, self.vx, self.vy, self.vz))

    def are_parallel(self, other: Hailstone) -> bool:
        return True if self.vx * other.vy == self.vy * other.vx else False

    def get_time_to_intersect(self, other: Hailstone) -> float:
        return (other.vy * (self.x - other.x) - other.vx * (self.y - other.y))  / \
                 (self.vy * other.vx - self.vx * other.vy)

    def intersect(self, other: Hailstone, limits: Tuple[int, int]):
        if self.are_parallel(other):
            return None
        else:
            t1 = self.get_time_to_intersect(other)
            t2 = other.get_time_to_intersect(self)
            if t1 < 0 or t2 < 0:
                return None

        point = (self.x + self.vx * t1, self.y + self.vy * t1)
        return point if \
            limits[0] <= point[0] <= limits[1] and limits[0] <= point[1] <= limits[1] \
            else None

    def get_row_of_A(self, other, type: str):
        if type == 'x-y':
            return [other.vy - self.vy, self.vx - other.vx, other.y - self.y, other.x - self.x]
        else:
            return [other.vz - self.vz, self.vx - other.vx, other.z - self.z, other.x - self.x]

    def get_element_of_b(self, other, type: str):
        if type == 'x-y':
            return self.y * self.vx - other.y * other.vx + other.x * other.vy - self.x * self.vy
        else:
            return self.z * self.vx - other.z * other.vx + other.x * other.vz - self.x * self.vz


if __name__ == "__main__":
    filename = 'input/Day24.txt'
    data = read_file(filename)

    limits = (200000000000000, 400000000000000)
    area = Area(limits, data, Part.PT1)
    print(f"The answer to part 1 is {area.get_intersections()}")

    # Part 2
    # I got pretty far on my own.  I was able to find for the sample data the correct
    # point by trying different velocities for the stone, and finding a point where all
    # the hailstones (with relative velocities) intersected with the stone in the x-y plane.
    # With enough time, this brute-force would have worked for real data. But it was never
    # going to finish. What I didn't realize is that we have way more hailstones than we
    # need.  So if I had just reduced the number of hailstones I was looking at I think
    # that approach could have worked although it would have been slow. But I lost faith
    # and looked at other solutions, and in the end solved two linear equations.
    print(f"The answer to part 2 is {area.find_stone()}")

