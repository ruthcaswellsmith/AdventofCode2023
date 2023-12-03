from __future__ import annotations

from enum import Enum, auto
from typing import List, Tuple, TypeVar, Union
from functools import total_ordering
import numpy as np
from collections import defaultdict
import re



T = TypeVar('T')
LARGE = 1_000_000


def read_file(file):
    with open(file, 'r') as f:
        return f.read().rstrip('\n').split('\n')


class Part(str, Enum):
    PT1 = auto()
    PT2 = auto()


class Orientation(str, Enum):
    X = 'X'
    Y = 'Y'
    Z = 'Z'


class Direction(str, Enum):
    RIGHT = auto()
    LEFT = auto()
    UP = auto()
    DOWN = auto()


class MapDirection(str, Enum):
    NORTH = 'N'
    SOUTH = 'S'
    EAST = 'E'
    WEST = 'W'
    NORTHEAST = 'NE'
    NORTHWEST = 'NW'
    SOUTHEAST = 'SE'
    SOUTHWEST = 'SW'


class Operator(str, Enum):
    ADD = '+'
    SUBTRACT = '-'
    DIVIDE = '/'
    MULTIPLY = '*'


class Node:
    def __init__(self, id: int, value: T):
        self.id = id
        self.value = value
        self.next = None
        self.previous = None


class CircularLinkedList:
    def __init__(self, elements: Union[str, List[T]]):
        self.nodes = [Node(i, ele) for i, ele in enumerate(elements)]
        self.head = self.nodes[0]
        self.tail = self.nodes[len(self.nodes) - 1]
        self.current = self.head
        for i in range(len(self.nodes)):
            self.current.next = self.nodes[i + 1] if i < len(self.nodes) - 1 else self.head
            self.current = self.current.next
        self.current = self.tail
        for i in range(len(self.nodes) - 1, -1, -1):
            self.current.previous = self.nodes[i - 1] if i > 0 else self.tail
            self.current = self.current.previous
        self.current = self.head

    def get_next(self):
        val = self.current.value
        self.current = self.current.next
        return val

    def get_node(self, num: int):
        if num == 0:
            return self.current
        current = self.current
        for _ in range(abs(num)):
            self.current = self.current.next if num > 0 else self.current.previous
        node = self.current
        self.current = current
        return node


@total_ordering
class EnhancedRange:
    def __init__(self, r: range):
        self.r = r

    def contains(self, other):
        return True if self.r[0] <= other.r[0] and self.r[-1] >= other.r[-1] else False

    def overlaps(self, other):
        rs = [self.r, other.r]
        rs.sort(key=lambda r: r[0])
        return True if rs[0][-1] >= rs[1][0] else False

    def combine(self, other):
        if not self.overlaps(other):
            raise ValueError('ranges do not overlap')
        return EnhancedRange(range(min([self.r[0], other.r[0]]), max([self.r[-1]+1, other.r[-1]+1])))

    def __lt__(self, other):
        return True if self.r[0] < other.r[0] or self.r[0] == other.r[0] and self.r[-1] < other.r[-1] else False

    def __eq__(self, other):
        return self.r[0] == other.r[0] and self.r[-1] == other.r[-1]


class XYPair:
    def __init__(self, xypair: Tuple[int, int]):
        self.x = xypair[0]
        self.y = xypair[1]

    @property
    def coordinates(self):
        return self.x, self.y

    def update(self, xypair: XYPair):
        self.x = xypair.x
        self.y = xypair.y

    def swap(self):
        temp = self.x
        self.x = self.y
        self.y = temp
        return self

    def manhattan(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)

    @property
    def id(self):
        return f'{self.x}-{self.y}'

    def move(self, direction: Direction):
        self.x += 1 if direction == Direction.RIGHT else -1 if direction == Direction.LEFT else 0
        self.y += 1 if direction == Direction.DOWN else -1 if direction == Direction.UP else 0

    def get_neighbor(self, direction: Direction) -> XYPair:
        return XYPair((self.x - 1, self.y)) if direction == Direction.LEFT else \
            XYPair((self.x + 1, self.y)) if direction == Direction.RIGHT else \
            XYPair((self.x, self.y - 1)) if direction == Direction.UP else \
            XYPair((self.x, self.y + 1))

    def get_inclusive_points_to(self, other: XYPair):
        if not( self.x == other.x or self.y == other.y):
            raise ValueError('Points are not vertically or horizontally aligned')
        if self.x == other.x:
            r = self.__get_inclusive_range(self.y, other.y)
            return [XYPair((self.x, y)) for y in r]
        r = self.__get_inclusive_range(self.x, other.x)
        return [XYPair((x, self.y)) for x in r]

    @staticmethod
    def __get_inclusive_range(x1: int, x2: int):
        return range(x1, x2 + 1) if x1 < x2 else range(x2, x1 + 1)

    def __sub__(self, other):
        return XYPair((self.x - other.x, self.y - other.y))

    def __eq__(self, other):
        return True if self.x == other.x and self.y == other.y else False

    def __hash__(self):
        return hash(self.x) + hash(self.y)


class XYZ:
    def __init__(self, xyz: Tuple[int, int, int]):
        self.x = xyz[0]
        self.y = xyz[1]
        self.z = xyz[2]

    @property
    def coordinates(self):
        return self.x, self.y, self.z

    def update(self, xyz: XYZ):
        self.x = xyz.x
        self.y = xyz.y
        self.z = xyz.z

    @property
    def id(self):
        return f'{self.x}-{self.y}-{self.z}'

    def __sub__(self, other):
        return XYZ((self.x - other.x, self.y - other.y, self.z - other.z))

    def __eq__(self, other):
        return True if self.x == other.x and self.y == other.y and self.z == other.z else False

    def __hash__(self):
        return hash(self.x) + hash(self.y) + hash(self.z)

    def manhattan(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y) + abs(self.z - other.z)


class GraphNode:
    def __init__(self, id: int, adj_list: List[int]):
        self.id = id
        self.adj_list = adj_list
        self.cost = LARGE


class Graph:
    def __init__(self, nodes: List[GraphNode], edge_costs: np.array):
        self.nodes = nodes
        self.edge_costs = edge_costs
        self.shortest_paths = edge_costs.copy()
        self.current_cost = 0
        self.visited = List[GraphNode]

    @property
    def num_nodes(self):
        return len(self.nodes)

    @property
    def unvisited_nodes(self):
        unvisited = [n for n in self.nodes if n not in self.visited]
        unvisited.sort(key=lambda n: n.cost)
        return unvisited

    def get_node(self, id: int):
        return next(iter(n for n in self.nodes if n.id == id))

    def find_all_shortest_paths(self):
        for n in self.nodes:
            self.__find_shortest_paths(n)

    def __find_shortest_paths(self, starting_node: GraphNode):
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

    def __get_unvisited_neighbors(self, current: GraphNode) -> List[GraphNode]:
        return [self.get_node(i) for i in current.adj_list if self.get_node(i) not in self.visited]

    def __update_costs_for_neighbors(self, current: GraphNode, neighbors: List[GraphNode]):
        for neighbor in neighbors:
            neighbor.cost = min(neighbor.cost,
                                current.cost + self.edge_costs[current.id, neighbor.id])


class CharRemover:
    def __init__(self, chars_to_remove):
        self.translation_table = str.maketrans("", "", chars_to_remove)

    def remove_chars(self, input_string):
        return input_string.translate(self.translation_table)


class CharReplacer:
    def __init__(self, chars_to_replace):
        self.translation_table = str.maketrans(chars_to_replace, ' ' * len(chars_to_replace))

    def replace_chars(self, input_string):
        return input_string.translate(self.translation_table)


def find_exact_match(number, input_string):
    pattern = fr'(?<!\d){re.escape(str(number))}(?!\d)'
    matches = re.finditer(pattern, input_string)

    match = next(matches, None)  # Get the desired occurrence
    return match.start() if match else None
