from utils import read_file, Part
from typing import List


class Report:
    def __init__(self, lines: List[List[int]], part: Part):
        self.part = part
        if self.part == Part.PT1:
            self.histories = [[line] for line in lines]
        else:
            self.histories = [[line[::-1]] for line in lines]

    @property
    def answer(self):
        return sum([line[0][-1] for line in self.histories])

    def get_diff(self, row: List[int], ind: int):
        return row[ind] - row[ind-1] if self.part == Part.PT1 else row[ind - 1] - row[ind]

    def get_new_val(self, row1: List[int], row2: List[int], ind: int):
        return row1[ind] + row2[ind] if self.part == Part.PT1 else row1[ind] - row2[ind]

    def get_differences(self):
        for history in self.histories:
            ind, row = 0, history[0]
            while not all([x == 0 for x in row]):
                history.append([self.get_diff(row, ind) for ind in range(1, len(row))])
                ind += 1
                row = history[ind]
        return self

    def extrapolate(self):
        for history in self.histories:
            ind = len(history) - 1
            bottom_row = history[ind]
            bottom_row.append(0)
            while ind > 0:
                ind -= 1
                curr_row = history[ind]
                max_ind = len(curr_row) - 1
                curr_row.append(self.get_new_val(curr_row, bottom_row, max_ind))
                bottom_row = curr_row


if __name__ == '__main__':
    filename = 'input/Day9.txt'
    data = read_file(filename)
    converted_data = [[int(ele) for ele in line.split()] for line in data]

    report = Report(converted_data, Part.PT1)
    report.get_differences().extrapolate()
    print(f"The answer to part 1 is {report.answer}.")

    report = Report(converted_data, Part.PT2)
    report.get_differences().extrapolate()
    print(f"The answer to part 2 is {report.answer}.")
