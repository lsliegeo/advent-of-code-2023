from util.input_util import get_input

EXAMPLE = """0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45"""


def lag(line: list[int]) -> list[int]:
    return [line[i + 1] - line[i] for i in range(len(line) - 1)]


def extrapolate_forwards(line: list[int]) -> int:
    result = 0
    while line and any(line):
        result += line[-1]
        line = lag(line)
    return result


def part1(input_data: str):
    lines = [list(map(int, line.split())) for line in input_data.splitlines()]
    return sum(extrapolate_forwards(line) for line in lines)


def extrapolate_backwards(line: list[int]) -> int:
    result = line[0]
    i = -1
    while line and any(line):
        line = lag(line)
        result += i * line[0]
        i *= -1
    return result


def part2(input_data: str):
    lines = [list(map(int, line.split())) for line in input_data.splitlines()]
    return sum(extrapolate_backwards(line) for line in lines)


if __name__ == '__main__':
    assert part1(EXAMPLE) == 114
    print(f'Solution for part 1 is: {part1(get_input())}')

    assert extrapolate_backwards([0, 3, 6, 9, 12, 15]) == -3
    assert extrapolate_backwards([1, 3, 6, 10, 15, 21]) == 0
    assert extrapolate_backwards([10, 13, 16, 21, 30, 45]) == 5

    assert part2(EXAMPLE) == 2
    print(f'Solution for part 2 is: {part2(get_input())}')
