from utils import read_file
from typing import List, Dict
from utils import get_range_intersection
from queue import Queue


class Almanac:
    def __init__(self, data: List[str]):
        line_num = 2
        self.maps = {}
        while line_num < len(data):
            map_type = data[line_num].replace(' map:', '')
            line_num += 1
            self.maps[map_type] = []
            while line_num < len(data) and data[line_num]:
                self.maps[map_type].append(Line(data[line_num]))
                line_num += 1
            line_num += 1
        seed_nums = [int(word) for word in data[0].split(':')[1].split()]
        self.seeds = [Seed(seed_num, self.maps) for seed_num in seed_nums]
        self.seed_ranges = [
                SeedRange(range(seed_nums[ind], seed_nums[ind] + seed_nums[ind + 1]), self.maps) for
                ind in range(0, len(seed_nums), 2)
            ]


class SeedRange:
    def __init__(self, seed_range: range, maps: Dict):
        self.seed_range = seed_range
        self.maps = maps

    @property
    def min_location(self):
        results = [self.seed_range]
        for map_type, lines in self.maps.items():
            results = self.process_map(lines, results)
        return min([r.start for r in results])

    @staticmethod
    def process_map(lines: List, results: List[range]):
        queue = Queue()
        [queue.put(r) for r in results]
        results = []
        for line in lines:
            unmatched = []
            while not queue.empty():
                r = queue.get()
                left, middle, right = \
                    get_range_intersection(r, range(line.source, line.source + line.range))
                if left:
                    unmatched.append(left)
                if right:
                    unmatched.append(right)
                if middle:
                    results.append(range(line.dest + middle.start - line.source,
                                         line.dest + middle.stop - line.source))
            for r in unmatched:
                queue.put(r)

        while not queue.empty():
            results.append(queue.get())

        return results


class Seed:
    def __init__(self, num: int, maps: Dict):
        self.num = num
        self.maps = maps

    @property
    def location(self):
        result = self.num
        for map_type, lines in self.maps.items():
            result = self.process_map(lines, result)
        return result

    @staticmethod
    def process_map(lines: List, result: int):
        for line in lines:
            if line.source <= result < line.source + line.range:
                return line.dest + result - line.source
        return result


class Line:
    def __init__(self, line: str):
        pts = [int(word) for word in line.split()]
        self.dest = pts[0]
        self.source = pts[1]
        self.range = pts[2]


if __name__ == '__main__':
    filename = 'input/Day5.txt'
    data = read_file(filename)

    almanac = Almanac(data)
    print(f"The answer to part 1 is {min([seed.location for seed in almanac.seeds])}")
    print(f"The answer to part 2 is {min([seed.min_location for seed in almanac.seed_ranges])}")



