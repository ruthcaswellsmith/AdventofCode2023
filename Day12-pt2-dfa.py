from utils import read_file
from enum import Enum
from typing import List, Dict

NUM_FOLDS = 5


class State(Dict, Enum):
    # this is a state that can take either input.  It circles to itself for a . and advances for a #
    EITHER = {'.': lambda x: x, '#': lambda x: x + 1}
    # this is a state that can only take a pound in which case it advances
    POUND_ONLY = {'#': lambda x: x + 1}
    # this is a state that can only take a dot in which case it advances
    DOT_ONLY = {'.': lambda x: x + 1}
    # this is the final state that can only take a dot and circles to itself
    FINAL = {'.': lambda x: x}


class Record:
    def __init__(self, springs: str, groups: List[int]):
        self.springs = springs
        self.groups = groups
        self.states = self.get_states()

    def get_states(self) -> List[Dict]:
        states = [State.EITHER]
        for g in self.groups[:-1]:
            for _ in range(g-1):
                states.append(State.POUND_ONLY)
            states.append(State.DOT_ONLY)
            states.append(State.EITHER)
        for _ in range(self.groups[-1]-1):
            states.append(State.POUND_ONLY)
        states.append(State.DOT_ONLY)
        states.append(State.FINAL)
        return states

    def get_matches(self):
        state_counts = {i: 0 for i in range(len(self.states))}
        state_counts[0] = 1

        for char in self.springs:
            new_state_counts = {i: 0 for i in range(len(self.states))}
            for curr_state, count in state_counts.items():
                if count == 0:
                    continue
                chars = ['.', '#'] if char == '?' else [char]
                for ch in chars:
                    callable = self.states[curr_state].get(ch, None)
                    if callable:
                        # This returns the new state number based on old state number and lambda
                        new_state = callable(curr_state)
                        new_state_counts[new_state] += state_counts[curr_state]
                    else:
                        # We cannot accept this input; this path is a dead end
                        pass
            state_counts = new_state_counts
        # Now our matches are the sum of the state counts for the final two states
        return state_counts[len(self.states)-1] + state_counts[len(self.states) - 2]


if __name__ == '__main__':
    filename = 'input/Day12.txt'
    data = read_file(filename)

    # Credit to Alex Oxorn for a very clear explanation of his solution which is really cool
    # https://alexoxorn.github.io/posts/aoc-day12-regular_languages/
    # Fun to learn about DFA and regular expressions and much clearer than lots of logic and recursion.
    records = []
    for line in data:
        pts = line.split(' ')
        springs = pts[0]
        groups = [int(ele) for ele in pts[1].split(',')]
        records.append(Record(springs, groups))
    print(f"The answer to part 1 is {sum([record.get_matches() for record in records])}.")

    new_records = []
    for record in records:
        springs = "?".join([record.springs] * 5)
        groups = record.groups * NUM_FOLDS
        new_records.append(Record(springs, groups))
    print(f"The answer to part 2 is {sum([record.get_matches() for record in new_records])}")
