from __future__ import annotations

from collections import defaultdict
from enum import Enum

from util.input_util import get_input

EXAMPLE = """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483"""


class Card(Enum):
    C2 = 2
    C3 = 3
    C4 = 4
    C5 = 5
    C6 = 6
    C7 = 7
    C8 = 8
    C9 = 9
    T = 10
    J = 11
    Q = 12
    K = 13
    A = 14

    @staticmethod
    def from_char(char: str) -> Card:
        if char.isdigit():
            char = 'C' + char
        return Card[char]

    @staticmethod
    def compare_string(card: Card) -> str:
        return f'{card.value:02}'


def parse_hand(hand_str: str) -> tuple[Card]:
    return tuple(Card.from_char(char) for char in hand_str)


def hand_score(cards: tuple[Enum]) -> tuple:
    hand_str = ''.join([Card.compare_string(c) for c in cards])
    value_to_count = defaultdict(int)
    for card in cards:
        value_to_count[card.value] += 1
    count_to_values = defaultdict(list)
    for value, count in value_to_count.items():
        count_to_values[count].append(value)

    if 5 in count_to_values:
        return 5, hand_str
    elif 4 in count_to_values:
        return 4, hand_str
    elif 3 in count_to_values:
        if 2 in count_to_values:
            # 3 + 2
            return 3, 2, hand_str
        else:
            # 3 + 1 + 1
            return 3, 1, 1, hand_str
    elif 2 in count_to_values:
        if len(count_to_values[2]) == 2:
            # 2 + 2 + 1
            return 2, 2, 1, hand_str
        else:
            # 2 + 1 + 1 + 1
            return 2, 1, 1, 1, hand_str
    else:
        return 1, hand_str


def part1(input_data: str):
    hand_to_bet = {
        parse_hand(line.split()[0]): int(line.split()[1])
        for line in input_data.splitlines()
    }

    result = 0
    for i, hand in enumerate(sorted(hand_to_bet, key=hand_score)):
        result += (i + 1) * hand_to_bet[hand]
    return result


def part2(input_data: str):
    pass


if __name__ == '__main__':
    assert hand_score(parse_hand('33332')) > hand_score(parse_hand('2AAAA'))
    assert hand_score(parse_hand('77888')) > hand_score(parse_hand('77788'))
    assert hand_score(parse_hand('KK677')) > hand_score(parse_hand('KTJJT'))
    assert hand_score(parse_hand('32456')) > hand_score(parse_hand('2345K'))

    assert part1(EXAMPLE) == 6440
    print(f'Solution for part 1 is: {part1(get_input())}')

    assert part2(EXAMPLE) == None
    print(f'Solution for part 2 is: {part2(get_input())}')
