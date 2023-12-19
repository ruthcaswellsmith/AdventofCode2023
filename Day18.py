from utils import read_file
from typing import List, Tuple
from collections import deque
import numpy as np
from shapely.geometry import Polygon, Point


SIZE = 1000
INITIAL = (500, 500)

DELTAS = {'R': (0, 1), 'L': (0, -1), 'U': (-1, 0), 'D': (1, 0)}


class Instruction:
    def __init__(self, line: str):
        pts = line.split()
        self.direction = pts[0]
        self.number = int(pts[1])
        self.color = pts[2]


class Trench:
    def __init__(self, data: List[str]):
        self.instructions = [Instruction(line) for line in data]
        self.grid = np.zeros((SIZE, SIZE), dtype=bool)
        self.pos = INITIAL

    def dig_trench(self):
        for instr in self.instructions:
            deltas = DELTAS[instr.direction]

            # Move in the direction we're going to be digging
            self.pos = (self.pos[0] + deltas[0], self.pos[1] + deltas[1])

            if instr.direction == 'R':
                self.grid[self.pos[0], self.pos[1]: self.pos[1] + instr.number] = True
            elif instr.direction == 'L':
                self.grid[self.pos[0], self.pos[1] - instr.number + 1: self.pos[1] + 1] = True
            elif instr.direction == 'U':
                self.grid[self.pos[0] - instr.number + 1: self.pos[0] + 1, self.pos[1]] = True
            else:
                self.grid[self.pos[0]: self.pos[0] + instr.number, self.pos[1]] = True

            # Move the amount we've dug
            self.pos = (self.pos[0] + (instr.number - 1) * deltas[0], self.pos[1] + (instr.number - 1) * deltas[1])

    @property
    def corner(self):
        return self.dimensions[0]

    @property
    def num_rows(self):
        return self.dimensions[1]

    @property
    def num_cols(self):
        return self.dimensions[2]

    @property
    def dimensions(self) -> Tuple[Tuple[int, int], int, int]:
        nonzero_indices = np.nonzero(self.grid)
        corner = np.min(nonzero_indices[0]), np.min(nonzero_indices[1])
        num_rows = np.max(nonzero_indices[0]) - corner[0] + 1
        num_cols = np.max(nonzero_indices[1]) - corner[1] + 1

        return corner, num_rows, num_cols

    def reset_grid(self):
        total_area = self.grid[self.corner[0]: self.corner[0] + self.num_rows,
                            self.corner[1]: self.corner[1] + self.num_cols]
        # reset our grid so it's centered on 0, 0
        self.grid = total_area.copy()

    def fill(self, i, j):
        stack = deque([(i, j)])

        while stack:
            current_i, current_j = stack.pop()
            self.grid[current_i, current_j] = True

            # Check and add neighbors to the stack if not filled
            if current_j + 1 < self.grid.shape[1] and not self.grid[current_i, current_j + 1]:
                stack.append((current_i, current_j + 1))
            if current_j - 1 >= 0 and not self.grid[current_i, current_j - 1]:
                stack.append((current_i, current_j - 1))
            if current_i + 1 < self.grid.shape[0] and not self.grid[current_i + 1, current_j]:
                stack.append((current_i + 1, current_j))
            if current_i - 1 >= 0 and not self.grid[current_i - 1, current_j]:
                stack.append((current_i - 1, current_j))


class Instruction2:
    def __init__(self, line: str):
        pts = line.split()
        self.direction = {'0': 'R', '1': 'D', '2': 'L', '3': 'U'}[pts[2][-2]]
        self.number = int(pts[2][2:7], 16)


class Trench2:
    def __init__(self, data: List[str]):
        self.instructions = [Instruction2(line) for line in data]
        self.pos = INITIAL
        self.vertices = [INITIAL]
        self.perimeter_area = 0

    @property
    def area(self):
        return int(self.polygon.area + self.perimeter_area // 2 + 1)

    @property
    def polygon(self):
        return Polygon(self.vertices)

    def dig_trench(self):
        for instr in self.instructions:
            deltas = DELTAS[instr.direction]

            # Move 1 spot in the direction we're digging
            self.pos = (self.pos[0] + deltas[0], self.pos[1] + deltas[1])

            # Move the amount we've dug
            self.pos = (self.pos[0] + (instr.number - 1) * deltas[0], self.pos[1] + (instr.number - 1) * deltas[1])

            self.perimeter_area += instr.number

            # Add our new position as a vertex
            self.vertices.append(self.pos)


if __name__ == "__main__":
    filename = 'input/Day18.txt'
    data = read_file(filename)

    trench = Trench(data)
    trench.dig_trench()
    trench.reset_grid()
    trench.fill(1, np.nonzero(trench.grid[0, :])[0][0] + 1)
    print(f"The answer to Part 1 is {trench.grid.sum().sum()}")

    trench2 = Trench2(data)
    trench2.dig_trench()
    print(f"The answer to Part 2 is {trench2.area}")
