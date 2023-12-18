import re

from util.grid_utils import Coordinate, DictGrid, Direction
from util.input_util import get_input

EXAMPLE = """R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)"""

CHAR_TO_DIRECTION = {
    'R': Direction.EAST,
    'D': Direction.SOUTH,
    'L': Direction.WEST,
    'U': Direction.NORTH,
}


def find_cell_inside(grid: DictGrid) -> Coordinate:
    for start_co in grid:
        for direction in Direction.orthogonal_directions():
            found_empty = False
            co = start_co
            while 1:
                prev_co, co = co, co.step(direction)
                if not grid.is_in_bounds(co):
                    break
                if co in grid:
                    if found_empty:
                        return prev_co
                    break
                else:
                    found_empty = True


def part1(input_data: str):
    grid = DictGrid()

    # Iterate border
    co = Coordinate(0, 0)
    for line in input_data.splitlines():
        char, amount, color = re.match('(.) (\d*) \((.*)\)', line).groups()
        direction = CHAR_TO_DIRECTION[char]
        for _ in range(int(amount)):
            co = co.step(direction)
            grid[co] = '#'

    # Fill inside
    to_explore: set[Coordinate] = {find_cell_inside(grid)}
    while to_explore:
        co = to_explore.pop()
        for direction in Direction.orthogonal_directions():
            next_co = co.step(direction)
            if next_co not in grid:
                grid[next_co] = '#'
                to_explore.add(next_co)

    return len(grid)


def part2(input_data: str):
    pass


if __name__ == '__main__':
    assert part1(EXAMPLE) == 62
    print(f'Solution for part 1 is: {part1(get_input())}')

    assert part2(EXAMPLE) == None
    print(f'Solution for part 2 is: {part2(get_input())}')
