from utils import read_file
from typing import List, Dict
import numpy as np

COLORS = ['blue', 'red', 'green']


class Game:
    def __init__(self, line: str):
        self.num = int(line.split()[1].replace(':', ""))
        self.subsets = self.__get_subsets(line)

    def __get_subsets(self, line: str):
        return [
            {pts[i + 1].replace(',', ''): int(pts[i]) for i in range(0, len(pts), 2)}
            for pts in [piece.split() for piece in " ".join(line.split()[2:]).split(";")]
        ]

    def is_possible(self, bag: Dict) -> bool:
        return all(bag[color] >= num for subset in self.subsets for color, num in subset.items())

    @property
    def fewest_cubes(self):
        return {color: max([subset.get(color, 0) for subset in self.subsets]) for color in COLORS}

    @property
    def power(self) -> int:
        return int(np.prod(list(self.fewest_cubes.values())))


class EntireGame:
    def __init__(self, games: List[Game], bag: Dict):
        self.games = games
        self.bag = bag

    @property
    def possible_games(self) -> List[int]:
        return [game.num for game in self.games if game.is_possible(self.bag)]

    @property
    def total_power(self) -> int:
        return sum([game.power for game in self.games])


if __name__ == '__main__':
    filename = 'input/Day2.txt'
    data = read_file(filename)

    bag = {'red': 12, 'green': 13, 'blue': 14}
    entire_game = EntireGame([Game(line) for line in data], bag)

    print(f"The answer to part 1 is {sum(entire_game.possible_games)}")

    print(f"The answer to part 2 is {entire_game.total_power}")



