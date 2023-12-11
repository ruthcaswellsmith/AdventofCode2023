from utils import read_file
from typing import List, Tuple
import bisect


class Image:
    def __init__(self, data: List[List[str]], offset: int):
        self.offset = offset
        self.rows_to_expand = [i for i, line in enumerate(data) if line.count('#') == 0]
        data = list(map(list, zip(*data)))
        self.cols_to_expand = [i for i, line in enumerate(data) if line.count('#') == 0]
        data = list(map(list, zip(*data)))
        self.galaxies = \
            [(i, j) for i, line in enumerate(data) for j, ele in enumerate(line) if ele == '#']
        self.pairs = {f"{i}-{j}": self.get_distance(left_loc, right_loc) for
                      i, left_loc in enumerate(self.galaxies[:-1], start=1) for
                      j, right_loc in enumerate(self.galaxies[i:], start=i+1)}

    def get_distance(self, source: Tuple, target: Tuple) -> int:
        distance = abs(source[0] - target[0]) + abs(source[1] - target[1])

        num1, num2 = min(source[0], target[0]), max(source[0], target[0])
        extra_rows = max(
            0,
            bisect.bisect_right(self.rows_to_expand, num2) -
            bisect.bisect_left(self.rows_to_expand, num1)
        )
        num1, num2 = min(source[1], target[1]), max(source[1], target[1])
        extra_cols = max(
            0,
            bisect.bisect_right(self.cols_to_expand, num2) -
            bisect.bisect_left(self.cols_to_expand, num1)
        )
        distance += self.offset * (extra_rows + extra_cols)

        return distance


if __name__ == '__main__':
    filename = 'input/Day11.txt'
    data = read_file(filename)

    image = Image(data, 1)
    print(f"The answer to part 1 is {sum(list(image.pairs.values()))}.")

    image = Image(data, 999_999)
    print(f"The answer to part 2 is {sum(list(image.pairs.values()))}.")
