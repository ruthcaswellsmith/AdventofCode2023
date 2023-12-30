from utils import read_file
import re
from typing import List
from functools import lru_cache


NUM_FOLDS = 5


class Record:
    def __init__(self, springs: str, groups_to_find: List[int]):
        self.springs = springs
        self.groups_to_find = groups_to_find
        self.pattern = re.compile(self.get_pattern())
        self.multiple_dots = re.compile(r'\.+')

    def get_pattern(self) -> str:
        pound_signs = ["".join(['#' for _ in range(group)]) for group in self.groups_to_find]
        pattern = "^[.]*"
        for pound_sign in pound_signs:
            pattern += pound_sign + "[.]+"
        pattern = pattern[:-1] + '*'
        pattern += "$"
        return pattern

    @lru_cache
    def find_matches(self, string: str):
        # If we have a complete string check if it matches
        if string.find('?') == -1:
            if self.pattern.match(string):
                return 1
            else:
                return 0

        # First check we don't have too many groups
        groups = [group for group in self.multiple_dots.split(string) if group != ""]
        definite_groups = [group for group in groups if '#' in group]
        if len(definite_groups) > len(self.groups_to_find):
            return 0

        # Now check that the groups we have so far match
        known_groups = re.findall('#+', string[:string.find('?')])
        if known_groups:
            if len(known_groups[-1]) > self.groups_to_find[len(known_groups)-1]:
                return 0
        results = 0
        for char in ['#', '.']:
            new_str = string.replace('?', char, 1)
            results += self.find_matches(new_str)
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
    print(f"The answer to part 1 is {sum(matches)}.")
