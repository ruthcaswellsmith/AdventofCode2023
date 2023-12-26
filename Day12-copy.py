from utils import read_file
import re
from typing import List
from functools import lru_cache
from itertools import takewhile
from functools import reduce
from operator import mul



NUM_FOLDS = 5


class Record:
    def __init__(self, springs: str, target_groups: List[int]):
        self.springs = springs
        self.groups = [g for g in springs.split('.') if g]
        self.target_groups = target_groups

    # @lru_cache
    def find_matches(self, groups: List[str], target_groups: List[int]) -> int:
        # If we have too many groups we return 0
        if len(groups) > len(target_groups):
            return 0

        # If our first group has too many pound signs return 0
        if self.count_pound_signs(groups[0]) > target_groups[0]:
            # we have too many initial pound signs
            return 0

        # If we don't have enough groups return 0
        if sum([self.max_groups(g) for g in groups]) < len(target_groups):
            return 0

        # If we have the right number of groups we can calculate the combinations
        if len(groups) == len(target_groups):
            return reduce(mul, [len(g) - target_groups[i] + 1 for i, g in enumerate(groups)])

        # Otherwise we sub in # and . for first ?
        g = groups[0]
        ind = g.find('?')
        return self.find_matches([groups[0].replace('?', '#', 1)] + groups[1:], target_groups) \
               + (self.find_matches([g[ind + 1:]] + groups[1:], target_groups[1:]) if ind > 0 else \
                self.find_matches([g[ind + 1:]] + groups[1:], target_groups))

    @staticmethod
    def count_pound_signs(string: str) -> int:
        match = re.match(r'^#+', string)
        return len(match.group()) if match else 0

    @staticmethod
    def max_groups(string: str) -> int:
        question_groups = re.findall(r'\?+', string[1:len(string) - 1])
        total_sum = 0
        for group in question_groups:
            num_question_marks = len(group)
            if num_question_marks % 2 == 0:
                total_sum += num_question_marks // 2
            else:
                total_sum += (num_question_marks // 2) + 1
        return total_sum + 1

        # # If we have a match we return 1
        # if [g.count('#') for g in groups] == target_groups:
        #     return 1

        # # Look at left group
        # g = groups[0]
        # if groups[0].count('#') > target_groups[0]:
        #     # we have too many pound signs
        #     return 0
        # if '?' not in g:
        #     # group is determined - it's a match or not
        #     if g.count('#') != target_groups[0]:
        #         return 0
        #     else:
        #         return self.find_matches(groups[1:], target_groups[1:])
        # else:
        #     # Sub in # or . for first ? mark
        #     ind = g.find('?')
        #     return self.find_matches([g.replace('?', '#', 1)] + groups[1:], target_groups) \
        #         + self.find_matches([g[0:ind], g[ind+1:]] + groups[1:], target_groups)


if __name__ == '__main__':
    filename = 'input/test.txt'
    data = read_file(filename)

    records = []
    for line in data:
        pts = line.split(' ')
        springs = pts[0]
        groups_to_find = [int(ele) for ele in pts[1].split(',')]
        records.append(Record(springs, groups_to_find))
    print(records[2].find_matches(records[2].groups, records[2].target_groups))
    #
    # matches = [record.matches for record in records]
    # print(f"The answer to part 1 is {sum([len(match) for match in matches])}.")

#     new_records = []
#     for i, record in enumerate(records):
#         new_groups_to_find = record.groups_to_find * NUM_FOLDS
#         new_springs = "?".join([record.springs for _ in range(NUM_FOLDS)])
#         new_records.append(Record(new_springs, new_groups_to_find))
#         print(i, len(new_records[-1].matches))
#     matches = [record.find_matches(record.springs) for record in new_records]
#     print(f"The answer to part 2 is {sum([len(match) for match in matches])}.")
# matches