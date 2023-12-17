from functools import lru_cache
from typing import List, Tuple

import numpy as np

from utils import read_file, MapDirection

LARGE = 1_000_000


class Node:
    def __init__(self, id: Tuple[int, int], adj_list: List[Tuple]):
        self.id = id
        self.adj_list = adj_list
        self.cost = LARGE


class Map:
    def __init__(self, data: np.array):
        self.max_x = len(data) - 1
        self.max_y = len(data[0]) - 1
        self.nodes = self.get_nodes(data)
        self.edge_costs = self.get_edge_costs(data)
        self.shortest_paths = self.edge_costs.copy()
        self.current_cost = 0
        self.visited: List[Node] = []
        self.direction = MapDirection.EAST
        self.steps = 1

    def get_nodes(self, data: List[List[str]]):
        nodes = []
        for i in range(len(data)):
            for j in range(len(data[0])):
                adj_list = [(i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1),
                    (i, j + 2), (i + 1, j + 1), (i - 1, j + 1),
                    (i, j - 2), (i + 1, j - 1), (i - 1, j - 1),
                    (i + 2, j), (i + 1, j - 1), (i + 1, j + 1),
                    (i - 2, j), (i - 1, j - 1), (i - 1, j + 1)
                    ]
                adj_list = list(set([ele for ele in adj_list if
                                     ele[0] >= 0 and ele[1] >= 0 and \
                                     ele[0] <= self.max_x and ele[1] <= self.max_y]))
                nodes += [Node((i, j), adj_list)]
        return nodes

    def get_edge_costs(self, data: List[List[str]]):
        edge_costs = {}
        for n1 in self.nodes:
            for id in n1.adj_list:
                n2 = self.get_node(id)
                if n1.id[0] == n2.id[0]:
                    edge_costs[(n1.id, n2.id)] = np.sum([data[n1.id[0], n1.id[1] + 1:n2.id[1] + 1]])
                elif n1.id[1] == n2.id[1]:
                    edge_costs[(n1.id, n2.id)] = np.sum([data[n1.id[0] + 1: n2.id[0] + 1, n1.id[1]]])
                else:
                    if n1.id[0] < n2.id[0] and n1.id[1] < n2.id[1]:
                        intermediates = [(n1.id[0] + 1, n1.id[1]), (n1.id[0], n1.id[1] + 1)]
                    elif n1.id[0] < n2.id[0] and n1.id[1] > n2.id[1]:
                        intermediates = [(n1.id[0] + 1, n1.id[1]), (n1.id[0], n1.id[1] - 1)]
                    elif n1.id[0] > n2.id[0] and n1.id[1] < n2.id[1]:
                        intermediates = [(n1.id[0] - 1, n1.id[1]), (n1.id[0], n1.id[1] + 1)]
                    else:
                        intermediates = [(n1.id[0] - 1, n1.id[1]), (n1.id[0], n1.id[1] - 1)]
                    edge_costs[(n1.id, n2.id)] = \
                        min([data[intermediate] for intermediate in intermediates]) + data[n2.id]
        return edge_costs

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

    @lru_cache()
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
            neighbors = self.__get_unvisited_neighbors(current)
            self.__update_costs_for_neighbors(current, neighbors)
            self.visited.append(current)
            if not len(self.visited) == self.num_nodes:
                current = self.unvisited_nodes[0]
            else:
                done = True
        for n in self.nodes:
            self.shortest_paths[starting_node.id, n.id] = n.cost
            self.shortest_paths[n.id, starting_node.id] = n.cost

    def __get_unvisited_neighbors(self, current: Node) -> List[Node]:
        return [self.get_node(i) for i in current.adj_list if self.get_node(i) not in self.visited]

    def __update_costs_for_neighbors(self, current: Node, neighbors: List[Node]):
        for neighbor in neighbors:
            neighbor.cost = min(neighbor.cost,
                                current.cost + self.edge_costs[current.id, neighbor.id])


if __name__ == "__main__":
    filename = 'input/test.txt'
    data = read_file(filename)

    city_map = Map(np.array([[int(ele) for ele in line] for line in data]))
    starting_node = city_map.get_node((0, 0))
    city_map.find_shortest_paths(starting_node)
    print(f"The answer to part 1 is "
          f"{city_map.shortest_paths[((0, 0), (city_map.max_x, city_map.max_y))]}")

