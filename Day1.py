from utils import read_file
from typing import List, Dict
import re


class CalibrationDocument:
    def __init__(self, lines: List[str], digits: Dict):
        self.data = [Line(line, digits) for line in lines]

    @property
    def calibration_value(self):
        return sum([line.calibration_value for line in self.data])


class Line:
    def __init__(self, line: str, digits: Dict):
        self.line = line
        self.digits = digits

    @property
    def occurrences(self):
        return {digit: [i.start() for i in re.finditer(digit, self.line)] for digit in self.digits}

    @property
    def first_digit(self):
        return min((k for k, v in self.occurrences.items() if v), key=lambda x: self.occurrences[x][0])

    @property
    def last_digit(self):
        return max((k for k, v in self.occurrences.items() if v), key=lambda x: self.occurrences[x][-1])

    @property
    def calibration_value(self):
        return int(self.digits[self.first_digit] + self.digits[self.last_digit])


if __name__ == '__main__':
    filename = 'input/Day1.txt'
    data = read_file(filename)

    valid_digits = {'1': '1', '2': '2', '3': '3', '4': '4', '5': '5', '6': '6', '7': '7', '8': '8', '9': '9'}
    doc = CalibrationDocument(data, valid_digits)
    print(f"The answer to part 1 is {doc.calibration_value}")

    valid_digits.update({'one': '1', 'two': '2', 'three': '3', 'four': '4', 'five': '5',
                         'six': '6', 'seven': '7', 'eight': '8', 'nine': '9'})
    doc = CalibrationDocument(data, valid_digits)
    print(f"The answer to part 2 is {doc.calibration_value}")

