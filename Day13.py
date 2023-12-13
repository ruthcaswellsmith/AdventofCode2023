from utils import read_file
from typing import List
import numpy as np
from enum import Enum, auto


class Direction(str, Enum):
    HORIZONTAL = auto()
    VERTICAL = auto()


class Pattern:
    def __init__(self, num: int, data: List[List[str]]):
        self.num = num
        self.pattern = np.array([[1 if ele == '#' else 0 for ele in line] for line in data])
        self.horizontal_ind = self.find_relected_line(Direction.HORIZONTAL)
        self.vertical_ind = self.find_relected_line(Direction.VERTICAL) if self.horizontal_ind is None else None
        self.score = self.vertical_ind + 1 if self.vertical_ind != None else 100 * (self.horizontal_ind + 1)

    def find_relected_line(self, direction: Direction):
        array = self.pattern if direction == Direction.HORIZONTAL else np.rot90(self.pattern, k=3)

        # Get indices where we have a reflection
        indices = []
        for ind in range(len(array) - 1):
            if np.array_equal(array[ind, :], array[ind+1, :]):
                indices.append(ind)
        if not indices:
            return

        for ind in indices:
            rows_to_check = min(ind, len(array) - ind - 2)
            reflects = True
            for i in range(1, rows_to_check + 1):
                if not np.array_equal(array[ind-i, :], array[ind+i+1, :]):
                    reflects = False
                    break
            if reflects:
                break
        return ind if reflects else None


if __name__ == '__main__':
    filename = 'input/Day13.txt'
    data = read_file(filename)

    empty_list_indices = [i for i, sublist in enumerate(data) if not sublist]
    ind = 0
    grids = []
    for i in empty_list_indices:
        grids.append(data[ind:i])
        ind = i + 1
    grids.append(data[ind:])

    patterns = [Pattern(num, line) for num, line in enumerate(grids)]
    print(f"The answer to part 1 is {sum([pattern.score for pattern in patterns])}.")
