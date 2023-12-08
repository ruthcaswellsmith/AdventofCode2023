from utils import read_file, Part
from typing import List, Callable
import math


class Node:
    def __init__(self, line: str):
        pts1 = line.split(' = ')
        self.name = pts1[0]
        pts2 = pts1[1].replace('(', "").replace(')', "").split(', ')
        self.L, self.R = pts2[0], pts2[1]

    def is_starting(self, part: Part):
        return self.name == 'AAA' if part == Part.PT1 else self.name[-1] == 'A'

    def is_ending(self, part: Part):
        return self.name == 'ZZZ' if part == Part.PT1 else self.name[-1] == 'Z'


class Map:
    def __init__(self, instructions: str, nodes: List[Node], part:Part):
        self.instructions = instructions
        self.num_instructions = len(self.instructions)
        self.nodes = {node.name: node for node in nodes}
        self.starting_nodes = [node for node in nodes if node.is_starting(part)]
        self.part = part

    def get_steps(self):
        num_steps = []
        for node in self.starting_nodes:
            num_steps.append(self.get_num_steps(node, lambda x: x.is_ending(self.part)))
        return num_steps

    def get_num_steps(self, starting_node: Node, reached_the_end: Callable):
        num, steps, loc = -1, 0, starting_node
        while not reached_the_end(loc):
            dir_to_go = self.instructions[
                (num := 0 if num == self.num_instructions - 1 else num + 1)]
            loc = self.nodes[getattr(self.nodes[loc.name], dir_to_go)]
            steps += 1
        return steps


if __name__ == '__main__':
    filename = 'input/Day8.txt'
    data = read_file(filename)
    instructions = data[0]
    nodes = [Node(line) for line in data[2:]]

    steps = Map(instructions, nodes, Part.PT1).get_steps()
    print(f"The answer to part 1 is {steps[0]}.")

    steps = Map(instructions, nodes, Part.PT2).get_steps()
    print(f"The answer to part 2 is {math.lcm(*steps)}.")
