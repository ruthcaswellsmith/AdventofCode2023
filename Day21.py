from __future__ import annotations

from collections import deque
from typing import List, Tuple

import numpy as np

from utils import read_file


class Garden:
    def __init__(self, data: List[str]):
        self.grid = np.array([[1 if ele == '#' else 0 if ele == '.' else 2 \
                               for ele in line] for line in data], dtype=int)
        self.max_x = self.grid.shape[0] - 1
        self.max_y = self.grid.shape[1] - 1
        self.start = np.where(self.grid == 2)[0][0], np.where(self.grid == 2)[1][0]
        self.grid = self.grid.astype(bool)
        self.grid[self.start] = False
        self.graph = self.build_graph()

    def build_graph(self):
        graph = {}
        for i in range(self.max_x + 1):
            for j in range(self.max_y + 1):
                if self.grid[i, j]:
                    continue
                neighbors = self.get_neighbors((i, j))
                graph[(i, j)] = set(neighbors)
        return graph

    def bfs(self, start, distance):
        visited = set()
        queue = deque([(start, 0)])
        result = []

        while queue:
            node, current_distance = queue.popleft()
            if node not in visited:
                visited.add(node)
                if current_distance == distance:
                    result.append(node)
                elif current_distance < distance:
                    queue.extend((neighbor, current_distance + 1) for \
                                 neighbor in self.graph[node] - visited)

        return len(result)

    def get_neighbors(self, pos: Tuple[int, int]):
        new_pos = []
        if pos[0] > 0 and not self.grid[(pos[0]-1, pos[1])]:
            new_pos.append((pos[0]-1, pos[1]))
        if pos[0] < self.max_x and not self.grid[(pos[0]+1, pos[1])]:
            new_pos.append((pos[0]+1, pos[1]))
        if pos[1] > 0 and not self.grid[(pos[0], pos[1]-1)]:
            new_pos.append((pos[0], pos[1]-1))
        if pos[1] < self.max_y and not self.grid[(pos[0], pos[1]+1)]:
            new_pos.append((pos[0], pos[1]+1))
        return new_pos


if __name__ == "__main__":
    filename = 'input/Day21.txt'
    data = read_file(filename)

    garden = Garden(data)

    # Part 1
    max_steps = 64
    reachable = sum([garden.bfs(garden.start, distance) for distance in range(0, max_steps + 1, 2)])
    print(f"The answer to Part 1 is {reachable}")

    # Part 2
    all_odd = sum([garden.bfs(garden.start, distance) for distance in range(0, garden.max_x + 1, 2)])
    all_even = sum([garden.bfs(garden.start, distance) for distance in range(1, garden.max_x + 1, 2)])

    corners_even = all_even - \
                   sum([garden.bfs(garden.start, distance) for distance in range(0, garden.max_x // 2, 2)])

    corners_odd = all_odd - \
                   sum([garden.bfs(garden.start, distance) for distance in range(1, garden.max_x // 2 + 1, 2)])

    n = (26501365 - (garden.max_x // 2)) / (garden.max_x + 1)
    total = int((n+1)**2 * all_odd + n**2 * all_even - (n+1) * corners_odd + n * corners_even)
    print(f"The answer to Part 2 is {total}")
