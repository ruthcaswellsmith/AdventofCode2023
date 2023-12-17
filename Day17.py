from utils import read_file, MapDirection
from typing import List, Tuple
import numpy as np


LARGE = 1_000_000


class Node:
    def __init__(self, id: Tuple[int, int], adj_list: List[Tuple[int, int]]):
        self.id = id
        self.adj_list = adj_list
        self.cost = LARGE
        self.direction = None
        self.steps = 0

    def __eq__(self, other):
        return True if self.id == other.id else False


class Graph:
    def __init__(self, data: np.array):
        self.nodes = self.__get_nodes()
        self.edge_costs = data
        self.shortest_paths = {}
        self.current_cost = 0
        self.visited: List[Node] = []

    def __get_nodes(self):
        nodes = []
        for i in range(len(data)):
            for j in range(len(data[0])):
                adj_list = [(i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)]
                adj_list = [t for t in adj_list if 0 <= t[0] < len(data) and 0 <= t[1] < len(data[0])]
                nodes.append(Node((i, j), adj_list))
        return nodes

    @property
    def num_nodes(self):
        return len(self.nodes)

    @property
    def unvisited_nodes(self):
        unvisited = [n for n in self.nodes if n not in self.visited]
        unvisited.sort(key=lambda n: n.cost)
        return unvisited

    def get_node(self, id: Tuple[int, int]):
        return next(iter(n for n in self.nodes if n.id == id))

    def find_all_shortest_paths(self):
        for n in self.nodes:
            self.find_shortest_paths(n)

    def find_shortest_paths(self, starting_node: Node):
        self.visited, self.current_cost = [], 0
        for n in self.nodes:
            n.cost = LARGE
        current = starting_node
        current.cost = 0

        done = False
        while not done:
            self.visited.append(current)
            neighbors = self.get_unvisited_neighbors(current)
            self.update_costs_for_neighbors(current, neighbors)
            if not len(self.visited) == self.num_nodes:
                current = self.unvisited_nodes[0]
            else:
                done = True
        for n in self.nodes:
            self.shortest_paths[f"{starting_node.id}-{n.id}"] = n.cost
            self.shortest_paths[f"{n.id}-{starting_node.id}"] = n.cost

    def get_unvisited_neighbors(self, current: Node) -> List[Node]:
        return [self.get_node(i) for i in current.adj_list if self.get_node(i) not in self.visited]

    @staticmethod
    def get_direction_of_neighbor(n1: Node, n2: Node) -> MapDirection:
        if n1.id[0] > n2.id[0]:
            return MapDirection.NORTH
        elif n1.id[0] < n2.id[0]:
            return MapDirection.SOUTH
        elif n1.id[1] > n2.id[1]:
            return MapDirection.WEST
        return MapDirection.EAST

    def update_costs_for_neighbors(self, current: Node, neighbors: List[Node]):
        for neighbor in neighbors:
            direction = self.get_direction_of_neighbor(current, neighbor)
            steps = current.steps + 1 if direction == current.direction else 1
            edge_cost = LARGE if steps == 4 else self.edge_costs[neighbor.id]
            neighbor.cost = min(neighbor.cost, current.cost + edge_cost)
            neighbor.direction = direction
            neighbor.steps = steps


if __name__ == "__main__":
    filename = 'input/test.txt'
    data = read_file(filename)

    graph = Graph(np.array([[int(ele) for ele in line] for line in data]))
    starting_node = graph.get_node((0, 0))
    starting_node.steps = 1
    starting_node.direction = MapDirection.EAST
    ending_node = graph.get_node((len(data) - 1, len(data[0]) - 1))
    graph.find_shortest_paths(starting_node)

    key = f'{starting_node.id}-{ending_node.id}'
    print(f"The answer to part 1 is {graph.shortest_paths[key]}")

