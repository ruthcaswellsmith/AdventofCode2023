from utils import read_file
import re
from typing import Tuple
from functools import lru_cache


NUM_FOLDS = 5


class Record:
    def __init__(self, springs: str, target_groups: Tuple):
        self.springs = springs
        self.target_groups = target_groups

    @lru_cache
    def find_matches(self, springs: str, target_groups: Tuple) -> int:
        groups = [g for g in springs.split('.') if g]

        if not target_groups:
            return 0 if '#' in springs else 1
        if not groups:
            return 0 if target_groups else 1

        # Make sure we don't have too many groups
        if len([g for g in groups if '#' in g]) > len(target_groups):
            return 0

        # Make sure we don't have too many # signs at the beginning
        match = re.match(r'^#+', groups[0])
        if match and len(match.group()) > target_groups[0]:
            return 0

        if springs[0] == '.':
            # If we start with a . we can drop it and continue
            return self.find_matches(springs[1:], target_groups)
        elif '?' not in groups[0]:
            # If we have a match on group[0] drop it and first target group
            if groups[0].count('#') == target_groups[0]:
                return self.find_matches('.'.join(groups[1:]), target_groups[1:])
            else:
                return 0
        else:
            # Return both . and # possibilities
            return \
                self.find_matches(springs.replace('?', '#', 1), target_groups) + \
                self.find_matches(springs.replace('?', '.', 1), target_groups)


if __name__ == '__main__':
    filename = 'input/Day12.txt'
    data = read_file(filename)

    records = []
    for line in data:
        pts = line.split(' ')
        springs = pts[0]
        target_groups = eval(pts[1])
        records.append(Record(springs, target_groups))
    print(sum([record.find_matches(record.springs, record.target_groups) for record in records]))

    new_records = []
    for i, record in enumerate(records):
        springs = "?".join([record.springs] * NUM_FOLDS)
        groups = record.target_groups * NUM_FOLDS
        new_records.append(Record(springs, groups))
    print(sum([record.find_matches(record.springs, record.target_groups) for record in new_records]))

