from utils import read_file
import numpy as np
import math


class Race:
    def __init__(self, time: int, record: int):
        self.time = time
        self.record = record

    @property
    def total_wins(self):
        return sum(self.wins)

    @property
    def wins(self):
        return [self.possible_distances[i] > self.record for i in range(self.time + 1)]

    @property
    def possible_distances(self):
        return [self.distance(hold) for hold in range(self.time + 1)]

    def distance(self, hold: int):
        return hold * (self.time - hold)


if __name__ == '__main__':
    filename = 'input/Day6.txt'
    data = read_file(filename)

    times = [int(word) for word in data[0].replace("Time:", "").split()]
    records = [int(word) for word in data[1].replace("Distance:", "").split()]

    races = [Race(times[i], records[i]) for i in range(len(times))]
    print(f"The answer to part 1 is {np.prod([race.total_wins for race in races])}")

    time = int(data[0].replace("Time:", "").replace(" ", ""))
    record = int(data[1].replace("Distance:", "").replace(" ", ""))
    min_time_to_win = math.ceil(-np.sqrt((time/2)**2 - record) + time/2)
    max_time_to_win = int(np.sqrt((time/2)**2 - record) + time/2)
    print(f"The answer to part 2 is {max_time_to_win - min_time_to_win + 1}")



