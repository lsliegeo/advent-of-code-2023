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


def parse_horizontal(lines: list[str]) -> list[str]:
    return lines


def parse_vertical(lines: list[str]) -> list[str]:
    return [''.join(line[i] for line in lines) for i in range(len(lines[0]))]


def get_reflection(values: list[str]) -> int | None:
    for i in range(1, len(values)):
        l = min(i, len(values) - i)
        if values[i - l:i] == values[i:i + l][::-1]:
            return i
    return None


def get_smudge_reflection(values: list[str]) -> int | None:
    for i in range(1, len(values)):
        l = min(i, len(values) - i)
        if (int(''.join(values[i - l:i]), 2) ^ int(''.join(values[i:i + l][::-1]), 2)).bit_count() == 1:
            return i
    return None


def part1(input_data: str):
    result = 0
    for lines in input_data.replace('.', '0').replace('#', '1').split('\n\n'):
        lines = lines.splitlines()
        if (reflection := get_reflection(parse_horizontal(lines))) is not None:
            result += 100 * reflection
        elif (reflection := get_reflection(parse_vertical(lines))) is not None:
            result += reflection
        else:
            raise Exception("Couldn't find a reflection")
    return result


def part2(input_data: str):
    result = 0
    for lines in input_data.replace('.', '0').replace('#', '1').split('\n\n'):
        lines = lines.splitlines()
        if reflection := get_smudge_reflection(parse_horizontal(lines)):
            result += 100 * reflection
        elif reflection := get_smudge_reflection(parse_vertical(lines)):
            result += reflection
        else:
            raise Exception("Couldn't find a smudge reflection")
    return result


if __name__ == '__main__':
    assert part1(EXAMPLE) == 5
    assert part1(EXAMPLE2) == 400
    assert part1(EXAMPLE + '\n\n' + EXAMPLE2) == 405
    print(f'Solution for part 1 is: {part1(get_input())}')

    assert part2(EXAMPLE) == 300
    assert part2(EXAMPLE2) == 100
    assert part2(EXAMPLE + '\n\n' + EXAMPLE2) == 400
    print(f'Solution for part 2 is: {part2(get_input())}')
