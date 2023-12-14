from util.input_util import get_input

EXAMPLE = """O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#...."""


def part1(input_data: str):
    columns = [[''] * len(input_data.splitlines()) for _ in range(len(input_data.splitlines()[0]))]
    for y, line in enumerate(input_data.splitlines()):
        for x, char in enumerate(line):
            columns[x][y] = char

    for column in columns:
        previous_empty_index = None
        for i, char in enumerate(column):
            if char == '#':
                previous_empty_index = None
            elif char == '.':
                if previous_empty_index is None:
                    previous_empty_index = i
            elif char == 'O':
                if previous_empty_index is not None:
                    column[previous_empty_index], column[i] = 'O', '.'
                    previous_empty_index += 1
            else:
                raise ValueError()

    return sum(len(columns) - i for column in columns for i, char in enumerate(column) if char == 'O')


def part2(input_data: str):
    pass


if __name__ == '__main__':
    assert part1(EXAMPLE) == 136
    print(f'Solution for part 1 is: {part1(get_input())}')

    assert part2(EXAMPLE) == None
    print(f'Solution for part 2 is: {part2(get_input())}')
