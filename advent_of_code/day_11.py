import itertools

from util.grid_utils import Coordinate
from util.input_util import get_input

EXAMPLE = """...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#....."""


def parse_input(input_data: str) -> list[Coordinate]:
    coordinates = []
    for x, line in enumerate(input_data.splitlines()):
        for y, char in enumerate(line):
            if char == '#':
                coordinates.append(Coordinate(x, y))
    return coordinates


def expand_empty_lines(input_data: str, expand_number: int) -> list[Coordinate]:
    expand_number = expand_number - 1
    coordinates = dict(enumerate(parse_input(input_data)))
    empty_horizontal_lines = {*range(max(co.x for co in coordinates.values()))} - {co.x for co in coordinates.values()}
    empty_vertical_lines = {*range(max(co.y for co in coordinates.values()))} - {co.y for co in coordinates.values()}

    while empty_horizontal_lines:
        x = empty_horizontal_lines.pop()
        for i, co in coordinates.items():
            if co.x >= x:
                coordinates[i] = Coordinate(co.x + expand_number, co.y)
        empty_horizontal_lines = {x2 + expand_number if x2 > x else x2 for x2 in empty_horizontal_lines}

    while empty_vertical_lines:
        y = empty_vertical_lines.pop()
        for i, co in coordinates.items():
            if co.y >= y:
                coordinates[i] = Coordinate(co.x, co.y + expand_number)
        empty_vertical_lines = {y2 + expand_number if y2 > y else y2 for y2 in empty_vertical_lines}

    return list(coordinates.values())


def expand_and_sum_distances(input_data: str, expand_number: int) -> int:
    coordinates = expand_empty_lines(input_data, expand_number)
    return sum(Coordinate.manhattan_distance(co_1, co_2) for co_1, co_2 in itertools.combinations(coordinates, 2))


def part1(input_data: str):
    return expand_and_sum_distances(input_data, 2)


def part2(input_data: str):
    return expand_and_sum_distances(input_data, 1000000)


if __name__ == '__main__':
    assert part1(EXAMPLE) == 374
    print(f'Solution for part 1 is: {part1(get_input())}')

    assert expand_and_sum_distances(EXAMPLE, 10) == 1030
    assert expand_and_sum_distances(EXAMPLE, 100) == 8410
    print(f'Solution for part 2 is: {part2(get_input())}')
