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


def part1(input_data: str):
    grid, start = parse_grid(input_data)
    loop_length = 0
    previous = None
    current = start
    while current != start or not loop_length:
        next_position = next(iter(
            neighbour_co
            for neighbour_co in coordinate_to_two_neighbours(grid, current)
            if neighbour_co != previous
        ))
        previous, current = current, next_position
        loop_length += 1

    return int(loop_length / 2)


def part2(input_data: str):
    pass


if __name__ == '__main__':
    assert part1(EXAMPLE) == 4
    assert part1(EXAMPLE2) == 8
    print(f'Solution for part 1 is: {part1(get_input())}')

    assert part2(EXAMPLE) == None
    print(f'Solution for part 2 is: {part2(get_input())}')
