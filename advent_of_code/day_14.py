from typing import Iterator

from util.grid_utils import Coordinate, Direction
from util.input_util import get_input

EXAMPLE = """O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#...."""


def part1(input_data: str):
    rows = from_input_data(input_data)
    return score(tilt(rows, Direction.NORTH))


def part2(input_data: str):
    input_data_to_index = {}
    i = 1000000000
    while i > 0:
        if (previous_index := input_data_to_index.get(input_data)) and i > previous_index - i:
            i %= previous_index - i
        else:
            input_data_to_index[input_data] = i
            input_data = tilt_4(input_data)
            i -= 1
    return score(from_input_data(input_data))


def from_input_data(input_data: str) -> list[list[str]]:
    return [list(line) for line in input_data.splitlines()]


def to_input_data(rows: list[list[str]]) -> str:
    return '\n'.join(''.join(row) for row in rows)


def score(rows: list[list[str]]) -> int:
    return sum(len(rows) - x for x, line in enumerate(rows) for char in line if char == 'O')


def tilt_4(input_data: str) -> str:
    rows = from_input_data(input_data)
    rows = tilt(rows, Direction.NORTH)
    rows = tilt(rows, Direction.WEST)
    rows = tilt(rows, Direction.SOUTH)
    rows = tilt(rows, Direction.EAST)
    return to_input_data(rows)


def tilt(rows: list[list[str]], direction: Direction) -> list[list[str]]:
    prev_co = None
    for co in iterate(rows, direction):
        if co is None:
            prev_co = None
        else:
            char = rows[co.x][co.y]
            if char == '#':
                prev_co = None
            elif char == '.':
                if prev_co is None:
                    prev_co = co
            else:
                if prev_co is not None:
                    rows[prev_co.x][prev_co.y], rows[co.x][co.y] = 'O', '.'
                    prev_co = prev_co.step(Direction.opposite(direction))
    return rows


def iterate(rows: list[list], direction: Direction) -> Iterator[Coordinate | None]:
    match direction:
        case Direction.NORTH:
            for y in range(len(rows[0])):
                for x in range(len(rows)):
                    yield Coordinate(x, y)
                yield None
        case Direction.SOUTH:
            for y in range(len(rows[0])):
                for x in reversed(range(len(rows))):
                    yield Coordinate(x, y)
                yield None
        case Direction.WEST:
            for x in range(len(rows)):
                for y in range(len(rows[0])):
                    yield Coordinate(x, y)
                yield None
        case Direction.EAST:
            for x in range(len(rows)):
                for y in reversed(range(len(rows[0]))):
                    yield Coordinate(x, y)
                yield None


if __name__ == '__main__':
    assert part1(EXAMPLE) == 136
    assert part1(get_input()) == 106648
    print(f'Solution for part 1 is: {part1(get_input())}')

    assert part2(EXAMPLE) == 64
    print(f'Solution for part 2 is: {part2(get_input())}')  # takes ~8 seconds to find a cycle
