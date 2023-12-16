from util.grid_utils import Coordinate, Direction, ListGrid
from util.input_util import get_input
from util.timer_util import ContextTimer

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


def explore(grid: ListGrid, start_co: Coordinate, start_direction: Direction) -> set[tuple[Coordinate, Direction]]:
    to_explore: list[tuple[Coordinate, Direction]] = [(start_co, start_direction)]
    explored: set[tuple[Coordinate, Direction]] = set()
    while to_explore:
        co, direction = to_explore.pop()
        explored.add((co, direction))
        char = grid[co.x][co.y]
        for next_direction in interact(direction, char):
            next_co = co.step(next_direction)
            if (next_co, next_direction) not in explored and grid.is_in_bounds(next_co):
                to_explore.append((next_co, next_direction))
    return explored


def number_energized(explored: set[tuple[Coordinate, Direction]]) -> int:
    return len(set(co for co, _ in explored))


def part1(input_data: str):
    grid = parse_grid(input_data)
    return number_energized(explore(grid, Coordinate(0, 0), Direction.EAST))


def part2(input_data: str):
    grid = parse_grid(input_data)
    best = 0

    for x in range(grid.max_x + 1):
        best = max(best, number_energized(explore(grid, Coordinate(x, 0), Direction.EAST)))
        best = max(best, number_energized(explore(grid, Coordinate(x, grid.max_y), Direction.WEST)))
    for y in range(grid.max_y + 1):
        best = max(best, number_energized(explore(grid, Coordinate(0, y), Direction.SOUTH)))
        best = max(best, number_energized(explore(grid, Coordinate(grid.max_x, y), Direction.NORTH)))
    return best


if __name__ == '__main__':
    assert part1(EXAMPLE) == 46
    print(f'Solution for part 1 is: {part1(get_input())}')

    assert part2(EXAMPLE) == 51
    with ContextTimer():
        print(f'Solution for part 2 is: {part2(get_input())}')
