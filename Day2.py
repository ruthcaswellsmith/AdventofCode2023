from utils import read_file
from typing import List, Dict
import re


class Game:
    def __init__(self, line: str):
        self.game = line.split()[1].replace(':', "")

        self.subsets = [Subset(text) for text in " ".join(line.split()[2:]).split(";")]

    def is_possible(self, bag: Dict):
        for subset in self.subsets:
            for color, num in subset.cubes.items():
                if bag[color] < num:
                    return False
        return True


class Subset:
    def __init__(self, text: str):
        pts = text.split()
        self.cubes = {pts[i + 1].replace(',', ''): int(pts[i]) for i in range(0, len(pts), 2)}


class EntireGame:
    def __init__(self, games: List[Game], bag: Dict):
        self.games = games
        self.bag = bag

    @property
    def possible_games(self) -> List[int]:
        return [ind + 1 for ind, val in
                enumerate([game.is_possible(self.bag) for game in self.games]) if val]

    @property
    def fewest_cubes(self):
        pass


if __name__ == '__main__':
    filename = 'input/test.txt'
    data = read_file(filename)

    bag = {'red': 12, 'green': 13, 'blue': 14}
    entire_game = EntireGame([Game(line) for line in data], bag)

    print(f"The answer to part 1 is {sum(entire_game.possible_games)}")


