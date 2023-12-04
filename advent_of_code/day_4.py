from util.input_util import get_input

EXAMPLE = """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"""


def part1(input_data: str):
    cards = [
        (
            [int(n) for n in line.split(': ')[1].split(' | ')[0].split()],
            [int(n) for n in line.split(': ')[1].split(' | ')[1].split()]
        )
        for line in input_data.splitlines()
    ]
    return sum(
        2 ** (number_matches - 1)
        for winning, current in cards
        if (number_matches := len(set(winning) & set(current))) > 0
    )


def part2(input_data: str):
    cards = [
        (
            [int(n) for n in line.split(': ')[1].split(' | ')[0].split()],
            [int(n) for n in line.split(': ')[1].split(' | ')[1].split()]
        )
        for line in input_data.splitlines()
    ]
    card_number_to_amount = {i: 1 for i in range(len(cards))}
    for i, (winning, current) in enumerate(cards):
        for j in range(len(set(winning) & set(current))):
            next_card_number = i + j + 1
            if next_card_number in card_number_to_amount:
                card_number_to_amount[next_card_number] += card_number_to_amount[i]
    return sum(card_number_to_amount.values())


if __name__ == '__main__':
    assert part1(EXAMPLE) == 13
    print(f'Solution for part 1 is: {part1(get_input())}')

    assert part2(EXAMPLE) == 30
    print(f'Solution for part 2 is: {part2(get_input())}')
