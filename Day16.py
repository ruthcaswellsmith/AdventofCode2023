from utils import read_file
from typing import Dict, Tuple, List
from queue import Queue

import numpy as np


class State:
    def __init__(self, symbol: str, pos: Tuple[int, int]):
        self.symbol = symbol
        self.x = pos[0]
        self.y = pos[1]


class Contraption:
    tiles = None
    max_positions = None
    mirrors: Dict[Tuple[int, int], str] = {}

    @classmethod
    def initialize_tiles(cls, data: List[str]):
        cls.max_positions = (len(data) - 1, len(data[0]) - 1)
        cls.tiles = {(i, j): {'>': False, '<': False, '^': False, 'v': False} for \
                     j in range(len(data[0])) for i in range(len(data))}

    @classmethod
    def initialize_mirrors(cls, data: List[str]):
        cls.mirrors = {(i, j): ele for i, line in enumerate(data) for \
                       j, ele in enumerate(line)}

    @classmethod
    def update_tiles(cls, state: State):
        cls.tiles[(state.x, state.y)][state.symbol] = True


class Beam:
    def __init__(self, state: State):
        self.state = state

    @property
    def pos(self):
        return self.state.x, self.state.y

    def travel(self):
        while True:
            # Check if we're off the grid
            if self.state.x < 0 or self.state.y < 0 or \
                    self.state.x > Contraption.max_positions[0] or \
                    self.state.y > Contraption.max_positions[1]:
                return []

            # Check if a beam with this state has been here before
            if Contraption.tiles[(self.state.x, self.state.y)][self.state.symbol]:
                return []

            # Update the grid to say we've visited this state
            Contraption.update_tiles(self.state)

            # Check if we've hit a splitter
            if Contraption.mirrors[self.pos] == '|' and self.state.symbol in ["<", ">"] or \
                    Contraption.mirrors[self.pos] == '-' and self.state.symbol in ["^", "v"]:
                return self.split(Contraption.mirrors[self.pos])

            # Otherwise update this beam and keep going
            self.state = self.get_new_position(Contraption.mirrors[self.pos])

    def split(self, symbol: str) -> List[State]:
        if symbol == '|':
            return [State('^', (self.state.x - 1, self.state.y)),
                    State('v', (self.state.x + 1, self.state.y))]
        else:
            return [State('<', (self.state.x, self.state.y - 1)),
                    State('>', (self.state.x, self.state.y + 1))]

    def get_new_position(self, symbol: str) -> State:
        if symbol == '.':
            if self.state.symbol == '>':
                return State('>', (self.state.x, self.state.y + 1))
            elif self.state.symbol == '<':
                return State('<', (self.state.x, self.state.y - 1))
            elif self.state.symbol == '^':
                return State('^', (self.state.x - 1, self.state.y))
            else:
                return State('v', (self.state.x + 1, self.state.y))

        elif symbol == '|':
            if self.state.symbol == '^':
                return State('^', (self.state.x - 1, self.state.y))
            else:
                return State('v', (self.state.x + 1, self.state.y))

        elif symbol == '-':
            if self.state.symbol == '>':
                return State('>', (self.state.x, self.state.y + 1))
            else:
                return State('<', (self.state.x, self.state.y - 1))

        elif symbol == "/":
            if self.state.symbol == '>':
                return State('^', (self.state.x - 1, self.state.y))
            elif self.state.symbol == '<':
                return State('v', (self.state.x + 1, self.state.y))
            elif self.state.symbol == '^':
                return State('>', (self.state.x, self.state.y + 1))
            else:
                return State('<', (self.state.x, self.state.y - 1))

        else:
            if self.state.symbol == '>':
                return State('v', (self.state.x + 1, self.state.y))
            elif self.state.symbol == '<':
                return State('^', (self.state.x - 1, self.state.y))
            elif self.state.symbol in ['^']:
                return State('<', (self.state.x, self.state.y - 1))
            else:
                return State('>', (self.state.x, self.state.y + 1))


def process_state(state: State) -> int:
    Contraption.initialize_tiles(data)
    Contraption.initialize_mirrors(data)

    queue = Queue()
    queue.put(Beam(state))

    while not queue.empty():
        beam = queue.get()
        new_states = beam.travel()
        for state in new_states:
            queue.put(Beam(state))

    energized_array = np.array([[sum(Contraption.tiles.get((i, j), {}).values()) \
                                 for j in range(Contraption.max_positions[1] + 1)] \
                                for i in range(Contraption.max_positions[0] + 1)], dtype=bool)
    return energized_array.sum().sum()


if __name__ == "__main__":
    filename = 'input/Day16.txt'
    data = read_file(filename)

    print(f"The answer to part 1 is {process_state(State('>', (0, 0)))}.")

    # Now we're going to start from each edge point
    starting_states = [State('v', (0, j)) for j in range(Contraption.max_positions[1] + 1)] + \
        [State('^', (Contraption.max_positions[0], j)) for j in range(Contraption.max_positions[1] + 1)] + \
        [State('>', (i, 0)) for i in range(Contraption.max_positions[0] + 1)] + \
        [State('<', (i, Contraption.max_positions[1])) for i in range(Contraption.max_positions[0] + 1)]

    energy_levels = []
    for state in starting_states:
        energy_levels.append(process_state(state))
    print(f"The answer to part 2 is {max(energy_levels)}.")
