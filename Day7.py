from utils import read_file, Part
from typing import List
from collections import Counter, defaultdict
from enum import Enum, auto


class HandType(str, Enum):
    HIGH_CARD = auto()
    ONE_PAIR = auto()
    TWO_PAIR = auto()
    THREE_OF_A_KIND = auto()
    FULL_HOUSE = auto()
    FOUR_OF_A_KIND = auto()
    FIVE_OF_A_KIND = auto()


CARD_VALUES = {'A': 13, 'K': 12, 'Q': 11, 'J': 10, 'T': 9, '9': 8,
               '8': 7, '7': 6, '6': 5, '5': 4, '4': 3, '3': 2, '2': 1}


class Hand:
    def __init__(self, cards: str, bid: int, part: Part):
        self.part = part
        self.dealt_cards = cards
        self.counter = Counter(self.dealt_cards)
        self.replaced_cards = self.replace_jokers()
        self.replaced_counter = Counter(self.replaced_cards)
        self.bid = bid
        self.rank = None

    def replace_jokers(self):
        max_key = max(self.counter, key=lambda k: self.counter[k] if k != 'J' else float('-inf'))
        return self.dealt_cards.replace('J', max_key)

    @property
    def hand_type(self):
        counter = self.counter if self.part == Part.PT1 else self.replaced_counter
        diff_cards, max_card_num = len(counter.keys()), max(counter.values())
        if diff_cards == 1:
            return HandType.FIVE_OF_A_KIND
        elif diff_cards == 2:
            return HandType.FOUR_OF_A_KIND if max_card_num == 4 else HandType.FULL_HOUSE
        elif diff_cards == 3:
            return HandType.THREE_OF_A_KIND if max_card_num == 3 else HandType.TWO_PAIR
        elif diff_cards == 4:
            return HandType.ONE_PAIR
        return HandType.HIGH_CARD


class Game:
    def __init__(self, hands: List[Hand], part: Part):
        self.hands = hands
        self.hand_types = defaultdict(list)
        [self.hand_types[hand.hand_type].append(hand) for hand in self.hands]
        self.card_values = CARD_VALUES if part == part.PT1 else \
            {k: v + 1 if i > 3 else v if i < 3 else 1 for i, (k, v) in enumerate(CARD_VALUES.items())}

    def rank_hands(self):
        highest_rank = 0
        for hand_type in HandType:
            sorted_hands = sorted(self.hand_types.get(hand_type, []),
                                  key=lambda x: [self.card_values[card] for card in
                                                 x.dealt_cards])
            for hand in sorted_hands:
                highest_rank += 1
                hand.rank = highest_rank


if __name__ == '__main__':
    filename = 'input/Day7.txt'
    data = read_file(filename)

    game = Game([Hand(line.split()[0], int(line.split()[1]), Part.PT1) for line in data], Part.PT1)
    game.rank_hands()
    print(f"The answer to part 1 is {sum([(hand.bid * hand.rank) for hand in game.hands])}")

    game = Game([Hand(line.split()[0], int(line.split()[1]), Part.PT2) for line in data], Part.PT2)
    game.rank_hands()
    print(f"The answer to part 2 is {sum([(hand.bid * hand.rank) for hand in game.hands])}")




