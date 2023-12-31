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


def compare_string_part_1(card: Card) -> str:
    value = card.value
    return f'{value:02}'


def compare_string_part_2(card: Card) -> str:
    value = card.value
    if card == Card.J:
        value = 1
    return f'{value:02}'


def parse_hand(hand_str: str) -> tuple[Card]:
    return tuple(Card.from_char(char) for char in hand_str)


def hand_score_1(cards: tuple[Card]) -> tuple:
    hand_str = ''.join([compare_string_part_1(c) for c in cards])
    value_to_count = defaultdict(int)
    for card in cards:
        value_to_count[card.value] += 1
    count_to_values = defaultdict(list)
    for value, count in value_to_count.items():
        count_to_values[count].append(value)

    if count_to_values[5]:
        return 5, hand_str
    elif count_to_values[4]:
        return 4, hand_str
    elif count_to_values[3]:
        if count_to_values[2]:
            # 3 + 2
            return 3, 2, hand_str
        else:
            # 3 + 1 + 1
            return 3, 1, hand_str
    elif count_to_values[2]:
        if len(count_to_values[2]) == 2:
            # 2 + 2 + 1
            return 2, 2, hand_str
        else:
            # 2 + 1 + 1 + 1
            return 2, 1, hand_str
    else:
        return 1, hand_str


def hand_score_2(cards: tuple[Card]) -> tuple:
    hand_str = ''.join([compare_string_part_2(c) for c in cards])
    value_to_count = defaultdict(int)
    most_frequent_non_joker = max([c for c in cards if c != Card.J], key=lambda c: cards.count(c), default=None)
    if most_frequent_non_joker is None:
        most_frequent_non_joker = Card.J
    for card in cards:
        if card == Card.J:
            value_to_count[most_frequent_non_joker.value] += 1
        else:
            value_to_count[card.value] += 1
    count_to_values = defaultdict(list)
    for value, count in value_to_count.items():
        count_to_values[count].append(value)

    if count_to_values[5]:
        return 5, hand_str
    elif count_to_values[4]:
        return 4, hand_str
    elif count_to_values[3]:
        if count_to_values[2]:
            # 3 + 2
            return 3, 2, hand_str
        else:
            # 3 + 1 + 1
            return 3, 1, hand_str
    elif count_to_values[2]:
        if len(count_to_values[2]) == 2:
            # 2 + 2 + 1
            return 2, 2, hand_str
        else:
            # 2 + 1 + 1 + 1
            return 2, 1, hand_str
    else:
        return 1, hand_str


def part1(input_data: str):
    hand_to_bet = {
        parse_hand(line.split()[0]): int(line.split()[1])
        for line in input_data.splitlines()
    }

    result = 0
    for i, hand in enumerate(sorted(hand_to_bet, key=hand_score_1)):
        result += (i + 1) * hand_to_bet[hand]
    return result


def part2(input_data: str):
    hand_to_bet = {
        parse_hand(line.split()[0]): int(line.split()[1])
        for line in input_data.splitlines()
    }

    result = 0
    for i, hand in enumerate(sorted(hand_to_bet, key=hand_score_2)):
        result += (i + 1) * hand_to_bet[hand]
    return result


if __name__ == '__main__':
    assert hand_score_1(parse_hand('33332')) > hand_score_1(parse_hand('2AAAA'))
    assert hand_score_1(parse_hand('77888')) > hand_score_1(parse_hand('77788'))
    assert hand_score_1(parse_hand('KK677')) > hand_score_1(parse_hand('KTJJT'))
    assert hand_score_1(parse_hand('32456')) > hand_score_1(parse_hand('2345K'))
    assert part1(EXAMPLE) == 6440
    print(f'Solution for part 1 is: {part1(get_input())}')

    assert hand_score_2(parse_hand('QQQQ2')) > hand_score_2(parse_hand('JKKK2'))
    assert hand_score_2(parse_hand('KK8AJ'))[:-1] == (3, 1)
    assert part2(EXAMPLE) == 5905
    print(f'Solution for part 2 is: {part2(get_input())}')
