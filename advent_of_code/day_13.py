from util.input_util import get_input

EXAMPLE = """#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#."""

EXAMPLE2 = """#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#"""


def horizontal_reflection(lines: list[str]) -> int | None:
    values = [sum((c == '#') * 2 ** i for i, c in enumerate(line[::-1])) for line in lines]
    return get_reflection(values)


def vertical_reflection(lines: list[str]) -> int | None:
    values = [sum((line[i] == '#') * 2 ** j for j, line in enumerate(lines)) for i in range(len(lines[0]))]
    return get_reflection(values)


def get_reflection(values: list[int]) -> int | None:
    for i in range(1, len(values)):
        l = min(i, len(values) - i)
        if values[i - l:i] == values[i:i + l][::-1]:
            return i
    return None


def part1(input_data: str):
    result = 0
    for lines in input_data.split('\n\n'):
        lines = lines.splitlines()
        if reflection := horizontal_reflection(lines):
            result += 100 * reflection
        elif reflection := vertical_reflection(lines):
            result += reflection
        else:
            raise Exception("Couldn't find a reflection")
    return result


def part2(input_data: str):
    pass


if __name__ == '__main__':
    assert vertical_reflection(EXAMPLE.splitlines()) == 5
    assert horizontal_reflection(EXAMPLE.splitlines()) is None
    assert vertical_reflection(EXAMPLE2.splitlines()) is None
    assert horizontal_reflection(EXAMPLE2.splitlines()) == 4
    assert part1(EXAMPLE + '\n\n' + EXAMPLE2) == 405
    print(f'Solution for part 1 is: {part1(get_input())}')

    assert part2(EXAMPLE) == None
    print(f'Solution for part 2 is: {part2(get_input())}')
