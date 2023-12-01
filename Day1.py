from utils import read_file
from typing import List, Dict
import re

BIG_NUM = 10_000


class CalibrationDocument:
    def __init__(self, data: List[str]):
        self.data = [Line(line) for line in data]

    @property
    def calibration_value(self):
        return sum([line.calibration_value for line in self.data])


class Line:
    def __init__(self, line: str):
        self.line = line

    @property
    def occurrences(self):
        return {digit: [i.start() for i in re.finditer(digit, self.line)] for digit in VALID_DIGITS}

    @property
    def first_digit(self, ):
        return min((k for k, v in self.occurrences.items() if v), key=lambda x: self.occurrences[x][0], default=None)

    @property
    def last_digit(self, ):
        return max((k for k, v in self.occurrences.items() if v), key=lambda x: self.occurrences[x][-1], default=None)

    @property
    def calibration_value(self):
        return int(VALID_DIGITS[self.first_digit] + VALID_DIGITS[self.last_digit])


if __name__ == '__main__':
    filename = 'input/Day1.txt'
    doc = CalibrationDocument(read_file(filename))
    VALID_DIGITS = {'1': '1', '2': '2', '3': '3', '4': '4', '5': '5', '6': '6', '7': '7', '8': '8', '9': '9'}
    print(f"The answer to part 1 is {doc.calibration_value}")
    VALID_DIGITS = {'1': '1', '2': '2', '3': '3', '4': '4', '5': '5', '6': '6', '7': '7', '8': '8', '9': '9',
                    'one': '1', 'two': '2', 'three': '3', 'four': '4', 'five': '5',
                    'six': '6', 'seven': '7', 'eight': '8', 'nine': '9'}
    print(f"The answer to part 2 is {doc.calibration_value}")

