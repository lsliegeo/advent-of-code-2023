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


def expand_empty_lines(input_data: str) -> str:
    lines = input_data.splitlines()

    # Expand empty horizontal lines
    i = 0
    while i < len(lines):
        line = lines[i]
        if '#' not in line:
            lines.insert(i, line)
            i += 1
        i += 1

    # Expand empty vertical lines
    i = 0
    while i < len(lines[0]):
        empty_vertical_line = all(line[i] == '.' for line in lines)
        if empty_vertical_line:
            for j, line in enumerate(lines):
                lines[j] = line[:i] + '.' + line[i:]
            i += 1
        i += 1

    return '\n'.join(lines)


def part1(input_data: str):
    input_data = expand_empty_lines(input_data)
    coordinates = parse_input(input_data)
    return sum(Coordinate.manhattan_distance(co_1, co_2) for co_1, co_2 in itertools.combinations(coordinates, 2))


def part2(input_data: str):
    pass


if __name__ == '__main__':
    assert expand_empty_lines("""...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....""") == """....#........
.........#...
#............
.............
.............
........#....
.#...........
............#
.............
.............
.........#...
#....#......."""
    assert part1(EXAMPLE) == 374
    print(f'Solution for part 1 is: {part1(get_input())}')

    assert part2(EXAMPLE) == None
    print(f'Solution for part 2 is: {part2(get_input())}')
