from __future__ import annotations

from utils import read_file, Part
from typing import Tuple
import heapq

import numpy as np


LARGE = 1_000_000


deltas = {0: (0, 1), 1: (1, 0), 2: (0, -1), 3: (-1, 0)}


class State:
    def __init__(self, pos: Tuple[int, int], direction: int, steps: int):
        self.pos = pos
        self.direction = direction
        self.steps = steps

    def __str__(self):
        return f"State({self.pos}, {self.direction}, {self.steps})"

    def __lt__(self, other: State):
        return self.steps < other.steps

    def __eq__(self, other: State):
        return self.pos is other.pos and \
               self.direction == other.direction and \
               self.steps == other.steps


class Graph:
    def __init__(self, costs: np.array, part: Part):
        self.part = part
        self.maxx, self.maxy = costs.shape
        self.edge_costs = costs
        self.total_costs = {}

    def find_shortest_path(self):
        state1, state2 = State((0, 0), 0, 0), State((0, 0), 1, 0)
        self.total_costs[str(state1)] = 0
        self.total_costs[str(state2)] = 0

        queue = [(0, state1), (0, state2)]
        while queue:
            cost, state = heapq.heappop(queue)

            if state.pos == (self.maxx - 1, self.maxy - 1):
                return self.total_costs[str(state)]

            if cost > self.total_costs[str(state)]:
                continue
            neighbors = self.get_neighbors(state, self.part)

            for neighbor in neighbors:
                new_cost = cost + self.edge_costs[neighbor.pos]
                if new_cost < self.total_costs.get(str(neighbor), LARGE):
                    self.total_costs[str(neighbor)] = new_cost
                    heapq.heappush(queue, (new_cost, neighbor))

    def get_neighbors(self, state: State, part: Part):
        neighbors = []
        if part == part.PT1:
            # we can always turn
            for delta_direction in [1, -1]:
                new_dir = (state.direction + delta_direction) % 4
                new_pos = self.get_new_position(state.pos, new_dir)
                neighbors.append(State(new_pos, new_dir, 1))
            # if we've taken fewer than three steps we can also continue straight
            if state.steps < 3:
                new_pos = self.get_new_position(state.pos, state.direction)
                neighbors.append(State(new_pos, state.direction, state.steps + 1))

        else:
            # if we have taken fewer than ten steps we can continue on
            if state.steps < 10:
                new_pos = self.get_new_position(state.pos, state.direction)
                # if the neighbor is the end state and we haven't taken at least 4 steps we
                # can't visit it
                if not (new_pos == (self.maxx-1, self.maxy-1) and state.steps < 4):
                    neighbors.append(State(new_pos, state.direction, state.steps + 1))

            if state.steps > 3:
                # if we have taken four steps in same direction we can turn
                for delta_direction in [1, -1]:
                    new_dir = (state.direction + delta_direction) % 4
                    new_pos = self.get_new_position(state.pos, new_dir)
                    neighbors.append(State(new_pos, new_dir, 1))

        # only return neighbors that are not off the grid
        return [n for n in neighbors if 0 <= n.pos[0] < self.maxx and 0 <= n.pos[1] < self.maxy]

    @staticmethod
    def get_new_position(pos: Tuple[int, int], direction: int) -> Tuple[int, int]:
        return pos[0] + deltas[direction][0], pos[1] + deltas[direction][1]


if __name__ == "__main__":
    filename = 'input/Day17.txt'
    data = read_file(filename)

    graph = Graph(np.array([[int(ele) for ele in line] for line in data]), Part.PT1)
    costs = [graph.find_shortest_path()]

    print(f"The answer to part 1 is {min(costs)}")

    graph = Graph(np.array([[int(ele) for ele in line] for line in data]), Part.PT2)
    costs = [graph.find_shortest_path()]

    print(f"The answer to part 2 is {min(costs)}")
