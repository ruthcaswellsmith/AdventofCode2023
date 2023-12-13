from utils import read_file
from typing import List
import numpy as np
from enum import Enum, auto


def parse_input(data: List[str]):
    empty_list_indices = [i for i, sublist in enumerate(data) if not sublist]
    ind = 0
    grids = []
    for i in empty_list_indices:
        grids.append(data[ind:i])
        ind = i + 1
    grids.append(data[ind:])

    grid_arrays = []
    for grid in grids:
        grid_arrays.append(np.array([[1 if ele == '#' else 0 for ele in line] for line in grid]))

    return grid_arrays


class Direction(str, Enum):
    HORIZONTAL = auto()
    VERTICAL = auto()


class Pattern:
    def __init__(self, num: int, pattern: np.array):
        self.num = num
        self.pattern = pattern
        self.horizontal_ind = self.find_relected_line(Direction.HORIZONTAL)
        self.vertical_ind = self.find_relected_line(Direction.VERTICAL) if self.horizontal_ind is None else None

    @property
    def score(self):
        if self.vertical_ind != None:
            return self.vertical_ind + 1
        if self.horizontal_ind != None:
            return 100 * (self.horizontal_ind + 1)

    def pattern_reflects(self, array: np.array, ind: int):
        rows_to_check = min(ind, len(array) - ind - 2)
        reflects = True
        for i in range(1, rows_to_check + 1):
            if not np.array_equal(array[ind - i, :], array[ind + i + 1, :]):
                reflects = False
                break
        return reflects

    def find_relected_line(self, direction: Direction):
        array = self.pattern if direction == Direction.HORIZONTAL else np.rot90(self.pattern, k=3)

        # Get indices where we have a reflection
        indices = []
        for ind in range(len(array) - 1):
            if np.array_equal(array[ind, :], array[ind+1, :]):
                indices.append(ind)
        if not indices:
            return

        reflects, ind = False, None
        for ind in indices:
            reflects = self.pattern_reflects(array, ind)
            if reflects:
                break

        return ind if reflects else None


if __name__ == '__main__':
    filename = 'input/Day13.txt'
    data = read_file(filename)
    grids = parse_input(data)

    patterns = [Pattern(num, grid) for num, grid in enumerate(grids)]
    print(f"The answer to part 1 is {sum([pattern.score for pattern in patterns])}.")

    counts = {}
    for pattern in patterns:
        count = 0

        array = pattern.pattern
        for i in range(array.shape[0]):
            for j in range(i + 1, array.shape[0]):
                if sum(array[i, :] != array[j, :]) == 1:
                    count += 1

        array = np.rot90(pattern.pattern, k=3)
        for i in range(array.shape[0]):
            for j in range(i + 1, array.shape[0]):
                if sum(array[i, :] != array[j, :]) == 1:
                    count += 1

        counts[pattern.num] = count
    print(1)



