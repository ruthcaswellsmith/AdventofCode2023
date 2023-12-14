from utils import read_file, MapDirection
import numpy as np
import hashlib

NUM_CYCLES = 1000000000


class Platform:
    def __init__(self, grid: np.array):
        self.grid = grid
        # We know grid is square (cheat!)
        self.size = grid.shape[0]
        self.grid_history = [(0, self.grid, self.load)]

    @property
    def load(self):
        return sum(sum(self.grid[i, :] == 0) * (self.size - i) for i in range(self.size))

    def cycle(self, n=1):
        i = 1
        while i < n + 1:
            for direction in [MapDirection.NORTH, MapDirection.WEST,
                              MapDirection.SOUTH, MapDirection.EAST]:
                self.tilt(direction)

            for prev in range(i):
                if np.array_equal(self.grid_history[prev][1], self.grid):
                    cycle = i - prev
                    ind = (n - prev) % cycle + prev
                    return self.grid_history[ind][2]
            self.grid_history.append((i, self.grid, self.load))
            i += 1

    def get_hash(self, arr: np.array) -> str:
        arr_bytes = arr.tobytes()
        hash_object = hashlib.sha256(arr_bytes)
        return hash_object.hexdigest()

    def tilt(self, d: MapDirection):
        k = 1 if d == MapDirection.NORTH else 0 if d == MapDirection.WEST else \
            3 if d == MapDirection.SOUTH else 2
        self.grid = np.rot90(self.grid, k=k)
        new_grid = []

        for i in range(self.size):
            row = self.grid[i, :]
            new_row = self.process_row(row)
            new_grid.append(new_row)

        self.grid = np.rot90(np.vstack(new_grid), k=-k)
        return self.load

    def process_row(self, row):
        new_row = []

        ind = np.where(row == 1)[0]
        if ind.size > 0 and ind[0] == 0:
            new_row.append(1)
            row = row[1:]

        while row.size > 0:
            ind = np.where(row == 1)[0]
            subset = row[:ind[0]] if ind.size > 0 else row
            row = row[ind[0] + 1:] if ind.size > 0 else np.array([])
            new_subset = self.let_rocks_roll(subset)
            new_row.extend(new_subset)

            if ind.size > 0:
                new_row.append(1)

        new_subset = self.let_rocks_roll(row)
        new_row.extend(new_subset)

        return np.array(new_row)

    @staticmethod
    def let_rocks_roll(subset: np.array):
        round_rocks = np.where(subset == 0)[0].shape[0]
        return np.concatenate((np.array([0] * round_rocks),
                                     np.array([None] * (len(subset) - round_rocks))))

    @staticmethod
    def calculate_load(subset: np.array, height: int) -> int:
        round_rocks = sum(subset == 0)
        return sum([l for l in range(height, height - round_rocks, -1)])


if __name__ == '__main__':
    filename = 'input/Day14.txt'
    data = read_file(filename)
    arr = np.array([[1 if ele == '#' else 0 if ele == 'O' else None for ele in line] for line in data])

    platform = Platform(arr)
    load = platform.tilt(MapDirection.NORTH)
    print(f"The answer to part 1 is {platform.load}.")

    platform = Platform(arr)
    print(f"The answer to part 2 is {platform.cycle(NUM_CYCLES)}")
