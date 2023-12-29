from __future__ import annotations

from utils import read_file
from collections import defaultdict
import random
import copy


if __name__ == "__main__":
    filename = 'input/Day25.txt'
    data = read_file(filename)

    orig_graph = defaultdict(set)
    for line in data:
        pts = line.split(':')
        for n in pts[1].split():
            orig_graph[pts[0]].add(n)
            orig_graph[n].add(pts[0])

    connections = []
    while len(connections) != 3:
        absorbed = defaultdict(set)
        graph = copy.deepcopy(orig_graph)
        while len(graph) > 2:
            n1 = random.choice(list(graph.keys()))
            # collapse one of its neighbors into it
            n2 = random.choice(list(graph[n1]))
            # remove n1 from n2's neighbor list and vice versa
            graph[n1].remove(n2)
            graph[n2].remove(n1)
            absorbed[n1] |= absorbed[n2]
            absorbed[n1].add(n2)
            del absorbed[n2]
            for n in graph[n2]:
                graph[n].remove(n2)
                graph[n].add(n1)
                if n != n1:
                    graph[n1].add(n)
            del graph[n2]

        # Form the groups
        groups = []
        for key, value_set in absorbed.items():
            new_set = value_set | {key}  # Union of the set with the key
            groups.append(new_set)
        if len(groups) == 1:
            # For some reason I sometimes end up with only one group but
            # I'm too tired to figure it out - something for later when I
            # miss AoC
            continue

        # Now see what the number of connections between the two groups are
        # Count how many times a node in group 1 connects to a node in group 2
        connections = []
        for node in groups[0]:
            for n in orig_graph[node]:
                if n in groups[1]:
                    connections.append(f"{node}-{n}")
    print(f"The answer to Part 1 is {len(groups[0])*len(groups[1])}.")
