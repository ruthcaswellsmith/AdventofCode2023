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
    def __init__(self, pattern: np.array, parent=None):
        self.pattern = pattern
        self.parent = parent
        self.cleaned_patterns = []
        self.horizontals = self.find_relected_lines(self.pattern)
        self.verticals = self.find_relected_lines(np.rot90(self.pattern, k=3))

    def update_array(self, arr1: np.array, arr2: np.array):
        ind = np.where(arr1 != arr2)[0][0]
        arr1[ind] = 0 if arr1[ind] == 1 else 0
        arr2[ind] = 0 if arr2[ind] == 1 else 0

    def add_cleaned_patterns(self, direction: Direction):
        max = self.pattern.shape[0] if direction == Direction.HORIZONTAL else \
            self.pattern.shape[1]

        for i in range(max):
            for k in range(i + 1, max):
                array = self.pattern.copy()
                arr1 = array[i, :] if direction == Direction.HORIZONTAL \
                    else array[:, i]
                arr2 = array[k, :] if direction == Direction.HORIZONTAL \
                    else array[:, k]
                if sum(arr1 != arr2) == 1:
                    self.update_array(arr1, arr2)
                    self.add_cleaned_pattern(array)

    def add_cleaned_pattern(self, cleaned_pattern: np.array):
        # Don't add the same child twice
        for pattern in self.cleaned_patterns:
            if np.array_equal(pattern.pattern, cleaned_pattern):
                return
        child = Pattern(cleaned_pattern, parent=self)
        self.cleaned_patterns.append(child)

    @property
    def score(self):
        h_to_ignore = self.parent.horizontals[0] if self.parent and self.parent.horizontals else None
        v_to_ignore = self.parent.verticals[0] if self.parent and self.parent.verticals else None
        horizontals = [line for line in self.horizontals if line != h_to_ignore] \
            if self.parent else self.horizontals
        verticals = [line for line in self.verticals if line != v_to_ignore] \
            if self.parent else self.verticals

        score = 0
        if horizontals:
            score += 100 * (horizontals[0] + 1)
        if verticals:
            score += verticals[0] + 1
        return score

    @staticmethod
    def pattern_reflects(array: np.array, ind: int):
        rows_to_check = min(ind, len(array) - ind - 2)
        reflects = True
        for i in range(1, rows_to_check + 1):
            if not np.array_equal(array[ind - i, :], array[ind + i + 1, :]):
                reflects = False
                break
        return reflects

    def find_relected_lines(self, array: np.array):
        # Get indices where two lines match
        indices = []
        for ind in range(len(array) - 1):
            if np.array_equal(array[ind, :], array[ind+1, :]):
                indices.append(ind)
        if not indices:
            return []

        lines_of_reflections = []
        for ind in indices:
            if self.pattern_reflects(array, ind):
                lines_of_reflections.append(ind)

        return lines_of_reflections


if __name__ == '__main__':
    filename = 'input/Day13.txt'
    data = read_file(filename)
    grids = parse_input(data)

    patterns = [Pattern(grid) for grid in grids]
    print(f"The answer to part 1 is {sum([pattern.score for pattern in patterns])}.")

    [pattern.add_cleaned_patterns(Direction.HORIZONTAL) for pattern in patterns]
    [pattern.add_cleaned_patterns(Direction.VERTICAL) for pattern in patterns]

    print(f"The answer to part 2 is "
          f"{sum(cleaned_pattern.score for pattern in patterns for cleaned_pattern in pattern.cleaned_patterns)}.")



