from utils import read_file
import re
from typing import List, Tuple
from functools import lru_cache
from functools import reduce
from operator import mul


NUM_FOLDS = 5
count = []


class Record:
    def __init__(self, springs: str, target_groups: List[int]):
        self.springs = springs
        self.groups = [g for g in springs.split('.') if g]
        self.target_groups = target_groups

    @lru_cache()
    def find_matches(self, groups: Tuple[str], target_groups: Tuple[int]) -> int:
        global count

        if isinstance(groups[0], tuple):
            print(5)
        # We have too many groups
        if len(groups) > len(target_groups):
            return 0

        # We have too many initial pound signs
        if self.count_pound_signs(groups[0]) > target_groups[0]:
            return 0

        # If we don't have enough groups return 0
        if sum([self.max_groups(g) for g in groups]) < len(target_groups):
            return 0

        # If we have the right number of groups
        if len(groups) == len(target_groups):
            if any([len(groups[i]) < target_groups[i] for i in range(len(groups))]):
                # If any of our groups don't have enough characters this is a dead end
                return 0
            else:
                # We can calculate the possible number of combinations
                val = reduce(mul, [len(g) - target_groups[i] + 1 for i, g in enumerate(groups)])
                count.append(val)
                return reduce(mul, [len(g) - target_groups[i] + 1 for i, g in enumerate(groups)])

        g = groups[0]
        ind = g.find('?')
        if ind == -1:
            # We have no more ? marks so first group must be a match.
            if len(g) == target_groups[0]:
                return self.find_matches(self.drop_first_group(groups), target_groups[1:])
            else:
                return 0
        else:
            # Replace the first ? with a #
            pound = self.find_matches(
                tuple([groups[0].replace('?', '#', 1)]) + self.drop_first_group(groups),
                target_groups
            )
            # Replace the first ? with a . and break it up into two groups
            # unless it's the first character in which case we just drop it
            g1, g2 = g[:ind], g[ind+1:]
            if not g1 and not g2:
                # We only had a ? so this is dead end
                dot = 0
            elif not g1:
                # we had a ? in first position, so if it's now a . we continue to search
                rem = (g2),
                dot = self.find_matches(
                    rem + self.drop_first_group(groups),
                    target_groups
                )
            else:
                # see if g1 is a match
                if len(g1) == target_groups[0]:
                    if not g2:
                        dot = self.find_matches(
                            self.drop_first_group(groups),
                            self.drop_first_group(target_groups)
                        )
                    else:
                        rem = (g2),
                        dot = self.find_matches(
                            rem + self.drop_first_group(groups),
                            self.drop_first_group(target_groups)
                        )
                else:
                    dot = 0
            return pound + dot

    @staticmethod
    def drop_first_group(t: Tuple) -> Tuple:
        return tuple([t[i] for i in range(1, len(t))])

    @staticmethod
    def count_pound_signs(string: str) -> int:
        try:
            match = re.match(r'^#+', string)
        except:
            print(4)
        return len(match.group()) if match else 0

    @staticmethod
    def max_groups(string: str) -> int:
        question_groups = re.findall(r'\?+', string[1:len(string) - 1])
        total_sum = 1
        for group in question_groups:
            num_question_marks = len(group)
            if num_question_marks % 2 == 0:
                total_sum += num_question_marks // 2
            else:
                total_sum += (num_question_marks // 2) + 1
        return total_sum


if __name__ == '__main__':
    filename = 'input/Day12.txt'
    data = read_file(filename)

    records = []
    for line in data:
        pts = line.split(' ')
        springs = pts[0]
        groups_to_find = [int(ele) for ele in pts[1].split(',')]
        records.append(Record(springs, groups_to_find))
    print(sum([record.find_matches(tuple(record.groups), tuple(record.target_groups)) for record in records]))

    new_records = []
    for i, record in enumerate(records):
        new_target_groups = record.target_groups * NUM_FOLDS
        new_springs = "?".join([record.springs for _ in range(NUM_FOLDS)])
        new_records.append(Record(new_springs, new_target_groups))
    print(sum([record.find_matches(tuple(record.groups), tuple(record.target_groups)) for record in new_records]))

