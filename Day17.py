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
                if i > 0:
                    adj_list.append((i - 1, j))
                    edge_costs[((i, j), (i - 1, j))] = costs[i - 1, j]
                    if i > 3:
                        adj_list.append((i - 3, j))
                        edge_costs[((i, j), (i - 3, j))] = LARGE
                if i < self.max_x:
                    adj_list.append((i + 1, j))
                    edge_costs[((i, j), (i + 1, j))] = costs[i + 1, j]
                    if i < self.max_x - 3:
                        adj_list.append((i + 3, j))
                        edge_costs[((i, j), (i + 3, j))] = LARGE
                if j > 0:
                    adj_list.append((i, j - 1))
                    edge_costs[((i, j), (i, j - 1))] = costs[i, j - 1]
                    if j > 3:
                        adj_list.append((i, j - 3))
                        edge_costs[((i, j), (i, j - 3))] = LARGE
                if j < self.max_y:
                    adj_list.append((i, j + 1))
                    edge_costs[((i, j), (i, j + 1))] = costs[i, j + 1]
                    if j < self.max_y - 3:
                        adj_list.append((i, j + 3))
                        edge_costs[((i, j), (i, j + 3))] = LARGE
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
    print(f"The answer to part 1 is "
          f"{city_map.shortest_paths[((0, 0), (city_map.max_x, city_map.max_y))]}")

