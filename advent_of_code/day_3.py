from util.grid_utils import Coordinate, Direction, Grid
from util.input_util import get_input

EXAMPLE = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598.."""


def parse_grid(grid_str: str) -> tuple[Grid, Grid]:
    # Could also be combined in a single grid, but then we'd have to look inside whether it's an int or a string
    symbols = Grid()
    for x, line in enumerate(grid_str.splitlines()):
        for y, char in enumerate(line):
            if char != '.' and not char.isdigit():
                symbols[Coordinate(x, y)] = char
    numbers = Grid()

    for x, line in enumerate(grid_str.splitlines()):
        number_str = None
        number_start_y = None
        for y, char in enumerate(line + '.'):
            # add an additional '.' to the line, so we can 'finish' and store numbers that end at the end of the line
            if char.isdigit():
                if number_str is None:
                    # Start of a new number
                    number_str = ''
                    number_start_y = y
                number_str += char
            else:
                if number_str is not None:
                    # End the previous number
                    numbers[Coordinate(x, number_start_y)] = int(number_str)
                    number_str = None

    return symbols, numbers


def number_neighbours(co: Coordinate, number: int) -> set[Coordinate]:
    """All neighbouring coordinates of a number and its start coordinate."""
    neighbours = []
    for _ in range(len(str(number))):
        neighbours += co.neighbours(diagonal=True).values()
        co = co.step(Direction.EAST)
    return set(neighbours)


def part1(input_data: str):
    symbols, numbers = parse_grid(input_data)
    # Sum of all numbers, which have a symbol in their neighbouring coordinates
    return sum(
        number
        for co, number in numbers.items()
        if any(
            neighbour in symbols
            for neighbour in number_neighbours(co, number)
        )
    )


def part2(input_data: str):
    symbols, numbers = parse_grid(input_data)
    result = 0
    # For the start coordinate of every number, a set of the neighbouring coordinates which are gears
    part_number_co_to_adjacent_gear_cos: dict[Coordinate, set[Coordinate]] = {
        co: {
            neighbour_co
            for neighbour_co in number_neighbours(co, number)
            if symbols.get(neighbour_co) == '*'
        }
        for co, number in numbers.items()
    }
    # For all gears
    for symbol_co, symbol in symbols.items():
        if symbol == '*':
            # The numbers which have this gear in one of their neighbouring coordinates
            adjacent_part_numbers = [
                numbers[part_number_co]
                for part_number_co, adjacent_gear_cos in part_number_co_to_adjacent_gear_cos.items()
                if symbol_co in adjacent_gear_cos
            ]
            if len(adjacent_part_numbers) == 2:
                result += adjacent_part_numbers[0] * adjacent_part_numbers[1]
    return result


if __name__ == '__main__':
    assert part1(EXAMPLE) == 4361
    print(f'Solution for part 1 is: {part1(get_input())}')

    assert part2(EXAMPLE) == 467835
    print(f'Solution for part 2 is: {part2(get_input())}')
