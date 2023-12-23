from __future__ import annotations

from typing import Tuple, Dict, Set
from queue import Queue

from utils import read_file, Part


class Graph:
    ARROWS = ['<', '>', '^', 'v']

    def __init__(self, data, part: Part):
        self.part = part
        self.deltas = {'<': (0, -1), '>': (0, 1), '^': (-1, 0), 'v': (1, 0)}
        self.grid = [[ele for ele in line] for line in data]
        self.dimensions = (len(data), len(data[0]))
        self.graph: Dict[Tuple[int, int]: Set[Tuple[int, int]]] = {}
        self.populate_graph(data)
        self.start = (0, 1)
        self.end = (len(data) - 1, len(data[0]) - 2)
        self.collapsed_graph: Dict = {}
        self.collapse_graph(self.start)
        self.visited = set()
        self.dp = {n: 0 for n in self.collapsed_graph.keys()}

    def collapse_graph(self, start: Tuple[int, int]):
        queue = Queue()
        queue.put((start, start, 0, {start}))
        seen_states = {(start, start, 0)}
        while not queue.empty():
            node, curr, dist, visited = queue.get()
            visited.add(curr)
            neighbors = [n for n in self.graph[curr] if n not in visited]
            # Travel until we hit a junction
            while len(neighbors) == 1:
                dist += 1
                curr = neighbors[0]
                visited.add(curr)
                neighbors = [n for n in self.graph[curr] if n not in visited]
            # We've hit a junction.  Add curr to collapsed graph and put neighbors
            # on the queue
            if node not in self.collapsed_graph:
                self.collapsed_graph[node] = {}
            if curr in self.collapsed_graph[node]:
                dist = max(dist, self.collapsed_graph[node][curr])
            self.collapsed_graph[node][curr] = dist
            for n in neighbors:
                if (curr, n, 1) not in seen_states:
                    queue.put((curr, n, 1, {curr}))
                    seen_states.add((curr, n, 1))
        self.collapsed_graph[self.end] = set()

    def populate_graph(self, data):
        for i in range(len(data)):
            for j in range(len(data[0])):
                if self.grid[i][j] != '#':
                    neighbors = self.get_neighbors(i, j, self.grid[i][j])
                    for n in neighbors:
                        self.add_edge((i, j), n)

    def get_neighbors(self, row: int, col: int, val: str) -> Set[Tuple[int, int]]:
        if self.part == Part.PT1:
            # If we are an arrow, only return the appropriate neighbor
            if val in self.ARROWS:
                return {(row + self.deltas[val][0], col + self.deltas[val][1])}
        # Otherwise look around
        neighbors = [(row + 1, col), (row -1, col), (row, col + 1), (row, col -1)]
        # Strip out points off the grid
        neighbors = [n for n in neighbors if 0 <= n[0] < self.dimensions[0] and 0 <= n[1] < self.dimensions[1]]
        # Strip out rocks
        neighbors = [n for n in neighbors if self.grid[n[0]][n[1]] != '#']
        if self.part == Part.PT2:
            return neighbors
        # For part 1 we strip out neighbors that are uphill
        new_neighbors = set()
        for n in neighbors:
            val = self.grid[n[0]][n[1]]
            if val == '.':
                new_neighbors.add(n)
            elif val in self.ARROWS:
                if self.deltas[val] == (n[0] - row, n[1] - col):
                    new_neighbors.add(n)
        return new_neighbors

    def add_edge(self, n1: Tuple[int, int], n2: Tuple[int, int]):
        if n1 not in self.graph:
            self.graph[n1] = set()
        self.graph[n1].add(n2)

    def dfs(self, node):
        if node == self.end:
            return 0

        max_dist = -float("inf")
        self.visited.add(node)
        for n in self.collapsed_graph[node]:
            if n not in self.visited:
                max_dist = max(max_dist, self.dfs(n) + self.collapsed_graph[node][n])
        self.visited.remove(node)

        return max_dist


if __name__ == "__main__":
    filename = 'input/Day23.txt'
    data = read_file(filename)

    graph = Graph(data, Part.PT1)
    dist = graph.dfs((0, 1))
    print(f"The answer to Part 1 is {dist}")

    graph = Graph(data, Part.PT2)
    dist = graph.dfs((0, 1))
    print(f"The answer to Part 1 is {dist}")
