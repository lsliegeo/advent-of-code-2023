import re

from util.grid_utils import Coordinate, Direction, Grid
from util.input_util import get_input

EXAMPLE = """.....
.S-7.
.|.|.
.L-J.
....."""

EXAMPLE2 = """..F7.
.FJ|.
SJ.L7
|F--J
LJ..."""

EXAMPLE3 = """...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
..........."""

EXAMPLE4 = """..........
.S------7.
.|F----7|.
.||....||.
.||....||.
.|L-7F-J|.
.|..||..|.
.L--JL--J.
.........."""

EXAMPLE5 = """.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ..."""

EXAMPLE6 = """FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L"""

CHAR_TO_DIRECTIONS: dict[str, tuple[Direction, Direction]] = {
    '|': (Direction.NORTH, Direction.SOUTH),
    '-': (Direction.WEST, Direction.EAST),
    'L': (Direction.NORTH, Direction.EAST),
    'J': (Direction.NORTH, Direction.WEST),
    '7': (Direction.SOUTH, Direction.WEST),
    'F': (Direction.SOUTH, Direction.EAST),
}


def coordinate_to_two_neighbours(grid: Grid, coordinate: Coordinate) -> tuple[Coordinate, Coordinate]:
    a, b = CHAR_TO_DIRECTIONS[grid.items[coordinate]]
    return coordinate.step(a), coordinate.step(b)


def parse_grid(input_data: str) -> tuple[Grid, Coordinate]:
    grid = Grid()
    start = None
    for x, line in enumerate(input_data.splitlines()):
        for y, char in enumerate(line):
            if char == 'S':
                start = Coordinate(x, y)
            elif char != '.':
                grid.items[Coordinate(x, y)] = char

    # We still need to find the correct character for the start
    directions_around_start_that_match = [
        direction
        for direction, neighbour_co in start.neighbours(diagonal=False).items()
        if neighbour_co in grid.items
           and start in coordinate_to_two_neighbours(grid, neighbour_co)
    ]
    start_char = next(iter(
        char for
        char, directions in CHAR_TO_DIRECTIONS.items()
        if sorted(directions_around_start_that_match, key=lambda d: d.name) == sorted(directions, key=lambda d: d.name)
    ))
    grid.items[start] = start_char

    return grid, start


def get_border(grid: Grid, start: Coordinate) -> set[Coordinate]:
    previous = None
    current = start
    border_positions = set()
    while current != start or previous is None:
        border_positions.add(current)
        next_position = next(iter(
            neighbour_co
            for neighbour_co in coordinate_to_two_neighbours(grid, current)
            if neighbour_co != previous
        ))
        previous, current = current, next_position
    return border_positions


def part1(input_data: str):
    grid, start = parse_grid(input_data)
    border_positions = get_border(grid, start)
    return int(len(border_positions) / 2)


def part2(input_data: str):
    grid, start = parse_grid(input_data)
    border_positions = get_border(grid, start)

    number_inside_using_logic = 0
    for x in range(0, grid.max_x + 1):
        inside = False
        on_a_line = False
        line_started_up = False
        max_relevant_y = max([co.y for co in grid.items if co.x == x], default=0)
        for y in range(0, max_relevant_y):
            current_coordinate = Coordinate(x, y)
            current_char = grid.items.get(current_coordinate) if current_coordinate in border_positions else None

            match current_char:
                case None:
                    if inside:
                        number_inside_using_logic += 1
                case '-':
                    pass
                case '|':
                    inside = not inside
                case _:
                    if on_a_line:
                        on_a_line = False
                        if line_started_up:
                            if Direction.SOUTH in CHAR_TO_DIRECTIONS[current_char]:
                                inside = not inside
                        else:
                            if Direction.NORTH in CHAR_TO_DIRECTIONS[current_char]:
                                inside = not inside
                    else:
                        on_a_line = True
                        line_started_up = Direction.NORTH in CHAR_TO_DIRECTIONS[current_char]

    number_inside_using_regex = 0
    lines = [
        ''.join([
            grid.items[Coordinate(x, y)] if Coordinate(x, y) in border_positions else '.'
            for y in range(grid.max_y + 1)
        ])
        for x in range(grid.max_x + 1)
    ]
    for x, line in enumerate(lines):
        line = re.sub(r'-*|L-*J|F-*7', '', line)  # remove --, F--J and L--7
        line = re.sub(r'[LF][J7]', '|', line)  # substitute F7 and LJ to |
        # line = re.sub(r'(^\.*)|(\.*$)', '', line)  # remove leading and trailing . (optional)

        inside = False
        for char in line:
            if char == '|':
                inside = not inside
            elif char == '.':
                if inside:
                    number_inside_using_regex += 1
            else:
                raise ValueError()

    assert number_inside_using_regex == number_inside_using_logic
    return number_inside_using_regex


if __name__ == '__main__':
    assert part1(EXAMPLE) == 4
    assert part1(EXAMPLE2) == 8
    print(f'Solution for part 1 is: {part1(get_input())}')

    assert part2(EXAMPLE3) == 4
    assert part2(EXAMPLE4) == 4
    assert part2(EXAMPLE5) == 8
    assert part2(EXAMPLE6) == 10
    print(f'Solution for part 2 is: {part2(get_input())}')
