from utils import read_file
import re
from typing import List, Tuple


class Record:
    def __init__(self, springs: str, groups_to_find: List[int]):
        self.springs = springs
        self.groups_to_find = groups_to_find
        self.pattern = self.get_pattern()

    def get_pattern(self) -> str:
        pound_signs = ["".join(['#' for i in range(group)]) for group in self.groups_to_find]
        pattern = "^[.]*"
        for pound_sign in pound_signs:
            pattern += pound_sign + "[.]+"
        pattern = pattern[:-1] + '*'
        pattern += "$"
        return pattern

    @staticmethod
    def groups(string: str) -> List[int]:
        matches = re.findall('#+', string)
        groups = [len(match) for match in matches]
        return groups

    def find_matches(self, string: str, memo=None):
        if memo is None:
            memo = {}

        if string in memo:
            return memo[string]

        # If we have a complete string check if it matches
        if string.find('?') == -1:
            if re.match(self.pattern, string):
                return [string]
            else:
                return []

        # Otherwise check if this is even a possibility
        groups = self.groups(string[:string.find('?')])
        if groups:
            if len(groups) > len(self.groups_to_find) or \
                    groups[-1] > self.groups_to_find[len(groups)-1]:
                return []
        results = []
        for char in ['#', '.']:
            new_str = string.replace('?', char, 1)
            results += self.find_matches(new_str, memo)
            memo[new_str] = results
        return results


if __name__ == '__main__':
    filename = 'input/Day12.txt'
    data = read_file(filename)

    records = []
    for line in data:
        pts = line.split(' ')
        springs = pts[0]
        groups_to_find = [int(ele) for ele in pts[1].split(',')]
        records.append(Record(springs, groups_to_find))
    matches = [record.find_matches(record.springs) for record in records]
    print(f"The answer to part 1 is {sum([len(match) for match in matches])}.")
#    print(f"The answer to part 2 is {2}.")

#    records = [Record(line, folds=5) for line in data]
