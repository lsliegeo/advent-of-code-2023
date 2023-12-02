import dataclasses
import re
from enum import Enum

from util.input_util import get_input

EXAMPLE = """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"""


class Color(Enum):
    GREEN = 'green'
    BLUE = 'blue'
    RED = 'red'


@dataclasses.dataclass
class Game:
    id: int
    rounds: list[dict[Color, int]]

    def is_possible_with(self, red: int, green: int, blue: int) -> bool:
        for round_ in self.rounds:
            if (
                round_.get(Color.RED, 0) > red
                or round_.get(Color.GREEN, 0) > green
                or round_.get(Color.BLUE, 0) > blue
            ):
                return False
        return True

    def power_of_minimum_required(self) -> int:
        red = green = blue = 0
        for round_ in self.rounds:
            red = max(red, round_.get(Color.RED, 0))
            green = max(green, round_.get(Color.GREEN, 0))
            blue = max(blue, round_.get(Color.BLUE, 0))
        return red * green * blue


def parse_games(input_data: str) -> list[Game]:
    games = []
    for line in input_data.splitlines():
        id_str, rounds_str = re.search('Game (\d+): (.*)', line).groups()
        games.append(Game(
            id=int(id_str),
            rounds=[
                {
                    Color(color_reveal.split(' ')[1]): int(color_reveal.split(' ')[0])
                    for color_reveal in round_str.split(', ')
                }
                for round_str in rounds_str.split('; ')
            ],
        ))
    return games


def part1(input_data: str):
    games = parse_games(input_data)
    return sum(game.id for game in games if game.is_possible_with(12, 13, 14))


def part2(input_data: str):
    games = parse_games(input_data)
    return sum(game.power_of_minimum_required() for game in games)


if __name__ == '__main__':
    assert part1(EXAMPLE) == 8
    print(f'Solution for part 1 is: {part1(get_input())}')

    assert part2(EXAMPLE) == 2286
    print(f'Solution for part 2 is: {part2(get_input())}')
