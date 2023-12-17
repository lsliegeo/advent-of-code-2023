import math

from util.grid_utils import Coordinate, Direction, ListGrid
from util.input_util import get_input

EXAMPLE = """2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533"""


def part1(input_data: str):
    heat_grid = ListGrid()
    grid = ListGrid()
    for line in input_data.splitlines():
        heat_grid.append(list(map(int, list(line))))
        grid.append([{d: math.inf for d in Direction.orthogonal_directions()} for _ in line])

    grid[0][0][Direction.EAST] = 0
    grid[0][0][Direction.SOUTH] = 0
    to_explore: set[tuple[Coordinate, Direction]] = {(Coordinate(0, 0), Direction.EAST), (Coordinate(0, 0), Direction.WEST)}

    while to_explore:
        if len(to_explore) % 1000 == 0:
            print(len(to_explore))
        co, direction = to_explore.pop()
        current_heat = grid[co.x][co.y][direction]
        for _ in range(3):
            co = co.step(direction)
            if not grid.is_in_bounds(co):
                break
            current_heat += heat_grid[co.x][co.y]
            for new_direction in (Direction.rotate(direction, True), Direction.rotate(direction, False)):
                if current_heat < grid[co.x][co.y][new_direction]:
                    grid[co.x][co.y][new_direction] = current_heat
                    to_explore.add((co, new_direction))


    return min(grid[grid.max_x][grid.max_y].values())


def part2(input_data: str):
    pass


if __name__ == '__main__':
    assert part1(EXAMPLE) == 102
    print(f'Solution for part 1 is: {part1(get_input())}')

    assert part2(EXAMPLE) == None
    print(f'Solution for part 2 is: {part2(get_input())}')
