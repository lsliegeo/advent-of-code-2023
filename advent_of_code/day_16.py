from util.grid_utils import Coordinate, Direction, ListGrid
from util.input_util import get_input

EXAMPLE = """.|...\....
|.-.\.....
.....|-...
........|.
..........
.........\\
..../.\\\..
.-.-/..|..
.|....-|.\\
..//.|...."""


def interact(direction: Direction, char: str) -> list[Direction]:
    match direction, char:
        case _, '.':
            return [direction]
        case (Direction.NORTH | Direction.SOUTH), '|':
            return [direction]
        case (Direction.EAST | Direction.WEST), '-':
            return [direction]
        case (Direction.NORTH | Direction.SOUTH), '-':
            return [Direction.rotate(direction, True), Direction.rotate(direction, False)]
        case (Direction.EAST | Direction.WEST), '|':
            return [Direction.rotate(direction, True), Direction.rotate(direction, False)]
        case (Direction.EAST | Direction.WEST), '/':
            return [Direction.rotate(direction, left=True)]
        case (Direction.NORTH | Direction.SOUTH), '/':
            return [Direction.rotate(direction, left=False)]
        case (Direction.EAST | Direction.WEST), '\\':
            return [Direction.rotate(direction, left=False)]
        case (Direction.NORTH | Direction.SOUTH), '\\':
            return [Direction.rotate(direction, left=True)]
        case _:
            raise Exception('Unexpected direction and/or character')


def parse_grid(input_data: str) -> ListGrid:
    grid = ListGrid()
    for line in input_data.splitlines():
        grid.append(list(line))
    return grid


def part1(input_data: str):
    grid = parse_grid(input_data)
    to_explore: list[tuple[Coordinate, Direction]] = [(Coordinate(0, 0), Direction.EAST)]
    explored: set[tuple[Coordinate, Direction]] = set()
    energized: set[Coordinate] = set()
    while to_explore:
        co, direction = to_explore.pop()
        explored.add((co, direction))
        energized.add(co)
        char = grid[co.x][co.y]
        for next_direction in interact(direction, char):
            next_co = co.step(next_direction)
            if (next_co, next_direction) not in explored and grid.is_in_bounds(next_co):
                to_explore.append((next_co, next_direction))

    return len(energized)


def part2(input_data: str):
    pass


if __name__ == '__main__':
    assert part1(EXAMPLE) == 46
    print(f'Solution for part 1 is: {part1(get_input())}')

    assert part2(EXAMPLE) == None
    print(f'Solution for part 2 is: {part2(get_input())}')
