import math

from util.grid_utils import Coordinate, Direction, ListGrid
from util.input_util import get_input
from util.timer_util import ContextTimer

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

EXAMPLE2 = """111111111111
999999999991
999999999991
999999999991
999999999991"""


def explore(input_data: str, first_turn_index: int, last_turn_index: int) -> int:
    """
    Pseudocode:

    start exploring in the top left
    while we still need to explore:
        get a position to explore from
        from that position, find where we can end up and do a turn
        for every turning point:
            if we found a faster way to arrive in this turning point:
                store the new heat value to arrive in this turning point
                add that turning point to the locations we need to explore
    """

    # heatgrid[x][y] = h
    # Coordinate (x, y) has heat h
    heat_grid: ListGrid[list[int]] = ListGrid()

    # distance_grid[x][y][d] = h
    # It takes h heat in order to start from (0, 0) and arrive in (x, y) with direction d
    distance_grid: ListGrid[list[dict[Direction, int]]] = ListGrid()

    for line in input_data.splitlines():
        heat_grid.append(list(map(int, list(line))))
        distance_grid.append([{d: math.inf for d in Direction.orthogonal_directions()} for _ in line])

    distance_grid[0][0][Direction.EAST] = 0
    distance_grid[0][0][Direction.SOUTH] = 0
    to_explore: set[tuple[Coordinate, Direction]] = {(Coordinate(0, 0), Direction.EAST), (Coordinate(0, 0), Direction.WEST)}

    while to_explore:
        # We simply store all positions to explore in a set
        # The order in which we explore has a major impact on the overall execution time
        # Using a set it takes roughly a minute, which is acceptable
        co, direction = to_explore.pop()
        current_heat = distance_grid[co.x][co.y][direction]
        for i in range(last_turn_index):
            co = co.step(direction)
            if not distance_grid.is_in_bounds(co):
                break
            current_heat += heat_grid[co.x][co.y]
            if i >= first_turn_index:
                for new_direction in (Direction.rotate(direction, True), Direction.rotate(direction, False)):
                    if current_heat < distance_grid[co.x][co.y][new_direction]:
                        distance_grid[co.x][co.y][new_direction] = current_heat
                        to_explore.add((co, new_direction))

    return min(distance_grid[distance_grid.max_x][distance_grid.max_y].values())


def part1(input_data: str):
    return explore(input_data, 0, 3)


def part2(input_data: str):
    return explore(input_data, 3, 10)


if __name__ == '__main__':
    assert part1(EXAMPLE) == 102
    assert part2(EXAMPLE) == 94
    assert part2(EXAMPLE2) == 71

    with ContextTimer():
        print(f'Solution for part 1 is: {part1(get_input())}')  # takes ~70 seconds
    with ContextTimer():
        print(f'Solution for part 2 is: {part2(get_input())}')  # takes ~70 seconds
