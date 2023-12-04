from utils import read_file
from typing import List


class Game:
    def __init__(self, data: List[str]):
        self.cards = [Card(line) for line in data]

    @property
    def num_cards(self):
        return len(self.cards)

    @property
    def answer_pt1(self):
        return sum([card.value for card in self.cards])

    @property
    def answer_pt2(self):
        return sum([card.count for card in self.cards])

    def play(self):
        card_num = 0
        while card_num < self.num_cards:
            card = self.cards[card_num]
            for ind in range(self.cards[card_num].num_winning_numbers):
                self.cards[card.num + ind].count += card.count
            card_num += 1


class Card:
    def __init__(self, line: str):
        pts1 = line.split(':')
        self.num = int(pts1[0].replace('Card ', ''))
        pts2 = pts1[1].split('|')
        self.winning = [int(num) for num in pts2[0].split()]
        self.numbers = [int(num) for num in pts2[1].split()]
        self.count = 1

    @property
    def num_winning_numbers(self):
        return sum(num in self.winning for num in self.numbers)

    @property
    def value(self):
        return int(2**(self.num_winning_numbers - 1))


if __name__ == '__main__':
    filename = 'input/Day4.txt'
    data = read_file(filename)

    game = Game(data)
    print(f"The answer to part 1 is {game.answer_pt1}")

    game.play()
    print(f"The answer to part 2 is {game.answer_pt2}")



