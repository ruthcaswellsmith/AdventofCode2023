from __future__ import annotations

import ast
from typing import List
from queue import Queue

from shapely.geometry import LineString, Point
from utils import read_file, XYZ


class Brick:
    def __init__(self, stack: Stack, id: int, line: str):
        self.id = id
        self.stack = stack
        start, end = map(ast.literal_eval, line.split('~'))
        self.start, self.end = XYZ(start), XYZ(end)
        self.resting_on: List[Brick] = []
        self.supporting: List[Brick] = []
        self.disintegratable = True

    @property
    def xy_point_or_segment(self):
        return Point(self.start.x, self.start.y) if \
            self.start.x == self.end.x and self.start.y == self.end.y else \
            LineString([(self.start.x, self.start.y), (self.end.x, self.end.y)])

    @property
    def minimum(self):
        return min(self.start.z, self.end.z)

    @property
    def maximum(self):
        return max(self.start.z, self.end.z)

    def can_fall(self) -> bool:
        if self.minimum == 1:
            return False

        for other in self.stack.get_bricks_one_level_below(self.id):
            if self.collides_with(other):
                self.resting_on.append(other)

        if not self.resting_on:
            return True

    def collides_with(self, other: Brick):
        return True if self.minimum - 1 in range(other.start.z, other.end.z + 1) and \
                       self.xy_point_or_segment.intersects(other.xy_point_or_segment) else False

    def determine_disintegratability(self):
        for brick in self.stack.get_bricks_one_level_above(self.id):
            if self.id in [b.id for b in brick.resting_on] and len(brick.resting_on) == 1:
                self.disintegratable = False

    def populate_supporting(self):
        pos = self.stack.get_position(self.id)
        for brick in self.stack.bricks[pos+1:]:
            if self in brick.resting_on:
                self.supporting.append(brick)


class Stack:
    def __init__(self, data: List[str]):
        self.bricks = [Brick(self, i, line) for i, line in enumerate(data)]
        self.bricks.sort(key=lambda x: x.minimum)

    @property
    def answer_pt2(self):
        essentials = [brick for brick in self.bricks if not brick.disintegratable]
        num = 0
        for essential in essentials:
            queue = Queue()
            queue.put(essential)
            resting_on = {brick.id: brick.resting_on.copy() for brick in stack.bricks}
            while not queue.empty():
                falling_brick = queue.get()
                for supported_brick in falling_brick.supporting:
                    resting_on[supported_brick.id].remove(falling_brick)
                    if not resting_on[supported_brick.id]:
                        num += 1
                        queue.put(supported_brick)
        return num

    def get_position(self, id: int):
        return next(iter([ind for ind, ele in enumerate(self.bricks) if ele.id == id]))

    def get_bricks_one_level_below(self, id: int):
        target_brick = self.get_brick(id)
        return [brick for brick in self.bricks if \
                brick.maximum + 1 == target_brick.minimum]

    def get_bricks_one_level_above(self, id: int):
        target_brick = self.get_brick(id)
        return [brick for brick in self.bricks if \
                brick.minimum == target_brick.maximum + 1]

    def get_brick(self, id: int):
        return next(iter([brick for brick in self.bricks if brick.id == id]))

    def let_bricks_fall(self):
        for i, brick in enumerate(self.bricks):
            while brick.can_fall():
                brick.start.z -= 1
                brick.end.z -= 1
        self.bricks.sort(key=lambda x: x.minimum)
        [brick.populate_supporting() for brick in self.bricks]
        [brick.determine_disintegratability() for brick in self.bricks]


if __name__ == "__main__":
    filename = 'input/Day22.txt'
    data = read_file(filename)

    stack = Stack(data)
    stack.let_bricks_fall()
    print(f"The answer to Part 1 is {sum([brick.disintegratable for brick in stack.bricks])}")

    print(f"The answer to Part 2 is {stack.answer_pt2}")