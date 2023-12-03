from utils import read_file
from typing import Dict, List
from utils import CharReplacer
import numpy as np
from utils import find_exact_match

SYMBOLS = '@#$%&*/+=-'


class Schematic:
    def __init__(self, data: str):
        self.char_replacer = CharReplacer(SYMBOLS + '.')
        self.lines = [line for line in data]
        self.grid = {i: {j: c for j, c in enumerate(line)} for i, line in enumerate(data)}
        self.max_x = len(self.grid[0])
        self.max_y = len(self.grid)
        self.numbers = self.__get_numbers()
        self.loc_to_numbers = {(num.x, num.y): num.value for num in self.numbers}
        self.gears = self.__get_gears()

    def __get_gears(self):
        gears = [Gear(i, j, nums)
                 for i in range(self.max_x)
                 for j in range(self.max_y)
                 if self.grid[i][j] == '*' and (nums := self.__get_touching_numbers(i, j))]
        return gears

    def __check_points(self, points: List, num_length: int) -> List:
        return [val for pt in points if (val := self.loc_to_numbers.get(pt)) and len(str(val)) == num_length]

    def __get_touching_numbers(self, row: int, col: int):
        # Check for 1-digit numbers first
        pts_to_check = [(row - 1, col + j) for j in range(-1, 2)] + \
            [(row, col - 1), (row, col + 1)] + \
            [(row + 1, col + j) for j in range(-1, 2)]
        touching_nums = self.__check_points(pts_to_check, 1)

        # Check for 2-digit numbers next
        pts_to_check = [(row - 1, col + j) for j in range(-2, 2)] + \
            [(row, col - 2), (row, col + 1)] + \
            [(row + 1, col + j) for j in range(-2, 2)]
        touching_nums.extend(self.__check_points(pts_to_check, 2))

        # Check for 3-digit numbers next
        pts_to_check = [(row - 1, col + j) for j in range(-3, 2)] + \
            [(row, col - 3), (row, col + 1)] + \
            [(row + 1, col + j) for j in range(-3, 2)]
        touching_nums.extend(self.__check_points(pts_to_check, 3))

        return touching_nums if len(touching_nums) == 2 else None

    def __get_numbers(self):
        numbers = []
        for i, line in enumerate(self.lines):
            line = self.char_replacer.replace_chars(line)
            words = [ele for ele in line.split(' ') if ele]
            for word_num, word in enumerate(words):
                j = find_exact_match(word, line)
                numbers.append(Number(self.grid, i, j, word))
        return numbers

    def answer_pt1(self):
        return sum([num.value for num in self.numbers if num.is_part_number()])

    def answer_pt2(self):
        return sum([gear.gear_ratio for gear in self.gears])


class Gear:
    def __init__(self, row: int, col: int, touching_numbers: List[int]):
        self.x = row
        self.y = col
        self.nums = touching_numbers

    @property
    def gear_ratio(self):
        return np.prod(self.nums)


class Number:
    def __init__(self, grid: Dict, row: int, col: int, word: str):
        self.grid = grid
        self.max_x = len(self.grid[0])
        self.max_y = len(self.grid)
        self.x = row
        self.y = col
        self.length = len(word)
        self.value = int(word)

    def is_part_number(self):
        if self.__sees_symbol(self.x, self.y):
            return True

    def __sees_symbol(self, row: int, col: int) -> bool:
        pts_to_check = []

        for j in range(col - 1, col + self.length + 1):
            # Check above
            pts_to_check.append((row - 1, j))

        for j in range(max(col - 1, 0), min(col + self.length, self.max_y - 1) + 1):
            # Check below
            pts_to_check.append((row + 1, j))

        # check left
        pts_to_check.append((row, col - 1))

        # check right
        pts_to_check.append((row, col + self.length))

        for pt in pts_to_check:
            if (val := self.grid.get(pt[0], {}).get(pt[1])) and val in SYMBOLS:
                return True


if __name__ == '__main__':
    filename = 'input/Day3.txt'
    data = read_file(filename)
    schematic = Schematic(data)
    print(f"The answer to part 1 is {schematic.answer_pt1()}")
    print(f"The answer to part 2 is {schematic.answer_pt2()}")
