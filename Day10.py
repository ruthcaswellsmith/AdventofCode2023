from utils import read_file, Part
from typing import List
import pandas as pd
import numpy as np


pipe_types = {
    '|': np.array([1, 0, 1, 0]),
    '-': np.array([0, 1, 0, 1]),
    'L': np.array([1, 1, 0, 0]),
    'J': np.array([1, 0, 0, 1]),
    '7': np.array([0, 0, 1, 1]),
    'F': np.array([0, 1, 1, 0]),
    '.': np.array([0, 0, 0, 0])
}

directions = {
    'NORTH': np.array([1, 0, 0, 0]),
    'EAST': np.array([0, 1, 0, 0]),
    'SOUTH': np.array([0, 0, 1, 0]),
    'WEST': np.array([0, 0, 0, 1])
}


class Sketch:
    def __init__(self, data: List[str]):
        self.grid = pd.DataFrame([[c for c in line] for line in data])
        self.max_x, self.max_y = self.grid.shape
        row, col = (self.grid == 'S').stack().idxmax()
        pipe_type = self.get_starting_pipe_type(row, col)
        openings = np.copy(pipe_types[pipe_type])
        # This will have two openings so close one so that we know which way to go
        openings[np.argmax(openings == 1)] = 0
        self.loop = Loop(self.grid, Pipe(row, col, pipe_type, openings))
        self.loop.build(None)

        # Below is for Part 2
        self.grid.iloc[row, col] = pipe_type
        self.is_in_loop = pd.DataFrame(np.full((self.max_x, self.max_y), False, dtype=bool))
        # traverse the loop
        while self.loop.current.next != self.loop.head:
            self.is_in_loop.iloc[self.loop.current.row, self.loop.current.col] = True
            self.loop.current = self.loop.current.next
        self.is_in_loop.iloc[self.loop.current.row, self.loop.current.col] = True
        self.loop.current = self.loop.current.next
        self.revised_grid = self.grid.where(self.is_in_loop, '.')
        self.final_grid = self.revised_grid.copy()
        for row_index, row in self.revised_grid.iterrows():
            on_edge = True
            for col_index, value in enumerate(list(row)):
                if value != '.':
                    on_edge = False
                else:
                    if on_edge:
                        self.final_grid.at[row_index, col_index] = 'O'
                    else:
                        new_value = self.is_inside_or_outside(row_index, col_index)
                        self.final_grid.at[row_index, col_index] = new_value

    def answer_pt2(self):
        return (self.final_grid == '*').sum().sum()

    def is_inside_or_outside(self, row: int, col: int):
        # we can look in any direction but we'll look to the right
        ray = "".join([ele.replace('\n', '') for ele in list(self.revised_grid.iloc[row, col + 1:])])
        ray = ray.replace('-', '').\
            replace('.', '').\
            replace('LJ', '').\
            replace('F7', '').\
            replace('L7', '|').\
            replace('FJ', '|')
        return 'O' if ray.count('|') % 2 == 0 else '*'

    def get_starting_pipe_type(self, row: int, col: int) -> str:
        openings = np.array([0, 0, 0, 0])

        if row > 0 and self.grid.iloc[row - 1, col] in ['|', '7', 'F']:
            # we can move north
            openings[0] = 1
        if col < self.max_y - 1 and self.grid.iloc[row, col + 1] in ['-', '7', 'J']:
            # we can move east
            openings[1] = 1
        if row < self.max_x - 1 and self.grid.iloc[row + 1, col] in ['|', 'L', 'J']:
            # we can move south
            openings[2] = 1
        if col > 0 and self.grid.iloc[row, col - 1] in ['-', 'L', 'F']:
            # we can move west
            openings[3] = 1

        return next((key for key, val in pipe_types.items() if np.array_equal(val, openings)), None)


class Pipe:
    def __init__(self, row: int, col: int, pipe_type: str, openings: np.array):
        self.row = row
        self.col = col
        self.pipe_type = pipe_type
        self.openings = openings
        self.next = None


class Loop:
    def __init__(self, grid: pd.DataFrame, head: Pipe):
        self.grid = grid
        self.head = head
        self.current = head
        self.num_pipes = 0

    def build(self, symbol: str):
        while symbol != 'S':
            if np.array_equal(self.current.openings, directions['NORTH']):
                row, col = self.current.row - 1, self.current.col
                symbol = self.grid.iloc[row, col]
                # block off south for next node
                openings = np.array([1, 1, 0, 1]) & np.copy(pipe_types.get(
                    self.head.pipe_type if symbol == 'S' else symbol))
            elif np.array_equal(self.current.openings, directions['EAST']):
                row, col = self.current.row, self.current.col + 1
                symbol = self.grid.iloc[row, col]
                # block off west for next node
                openings = np.array([1, 1, 1, 0]) & np.copy(pipe_types.get(
                    self.head.pipe_type if symbol == 'S' else symbol))
            elif np.array_equal(self.current.openings, directions['SOUTH']):
                row, col = self.current.row + 1, self.current.col
                symbol = self.grid.iloc[row, col]
                # block off north for next node
                openings = np.array([0, 1, 1, 1]) & np.copy(pipe_types.get(
                    self.head.pipe_type if symbol == 'S' else symbol))
            else:
                row, col = self.current.row, self.current.col - 1
                symbol = self.grid.iloc[row, col]
                # block off east for next node
                openings = np.array([1, 0, 1, 1]) & np.copy(pipe_types.get(
                    self.head.pipe_type if symbol == 'S' else symbol))

            if symbol == 'S':
                self.current.next = self.head
                self.current = self.head
            else:
                self.current.next = Pipe(row, col, symbol, openings)
                self.current = self.current.next
            self.num_pipes += 1


if __name__ == '__main__':
    filename = 'input/Day10.txt'
    data = read_file(filename)
    sketch = Sketch(data)

    print(f"The answer to part 1 is {sketch.loop.num_pipes // 2}.")

    print(f"The answer to part 2 is {sketch.answer_pt2()}.")
