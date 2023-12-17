from utils import read_file, MapDirection
from typing import List, Tuple

import numpy as np

LARGE = 1_000_000


class Node:
    def __init__(self, id: Tuple[int, int], adj_list: List[Tuple]):
        self.id = id
        self.adj_list = adj_list
        self.cost = LARGE


class Map:
    def __init__(self, data: List[List[str]]):
        self.max_x = len(data) - 1
        self.max_y = len(data[0]) - 1
        self.nodes, self.edge_costs = self.get_nodes_and_edge_costs(data)
        self.shortest_paths = self.edge_costs.copy()
        self.current_cost = 0
        self.visited: List[Node] = []
        self.direction = MapDirection.EAST
        self.steps = 1

    def get_nodes_and_edge_costs(self, data: List[List[str]]):
        nodes = []
        edge_costs = {}
        costs = np.array([[int(ele) for ele in line] for line in data])
        for i in range(len(data)):
            for j in range(len(data[0])):
                adj_list = []
                for ind in range(1, min(5, self.max_y - j + 1)):
                    # grab nodes to the right
                    edge_costs[((i, j), (i, j + ind))] = LARGE if ind == 4 else \
                        sum(costs[i, j + 1: j + 1 + ind])
                    adj_list.append((i, j + ind))
                for ind in range(1, min(5, j + 1)):
                    # grab nodes to the left
                    edge_costs[((i, j), (i, j - ind))] = LARGE if ind == 4 else \
                        sum(costs[i, j - ind: j])
                    adj_list.append((i, j - ind))
                for ind in range(1, min(5, self.max_x - i + 1)):
                    edge_costs[((i, j), (i + ind, j))] = LARGE if ind == 4 else \
                        sum(costs[i + 1: i + 1 + ind, j])
                    adj_list.append((i + ind, j))
                for ind in range(1, min(5, i + 1)):
                    edge_costs[((i, j), (i - ind, j))] = LARGE if ind == 4 else \
                        sum(costs[i - ind: i, j])
                    adj_list.append((i - ind, j))
                nodes += [Node((i, j), adj_list)]
        return nodes, edge_costs

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
            self.__find_shortest_paths(n)

    def __find_shortest_paths(self, starting_node: Node):
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

    city_map = Map(data)
    city_map.find_all_shortest_paths()
    print(1)
