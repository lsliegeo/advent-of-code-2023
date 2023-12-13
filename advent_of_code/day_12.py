import functools
import re

from util.input_util import get_input

EXAMPLE = """???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1"""


@functools.cache
def get_num_matches(line: str, groups: tuple[int]) -> int:
    line = re.sub('^\.*', '', line)
    if not groups:
        return '#' not in line
    if not line:
        return 0

    s = 0
    if re.match(f'[?#]{{{groups[0]}}}[?.]', line):
        s += get_num_matches(line[groups[0] + 1:], groups[1:])
    if line[0] == '?':
        s += get_num_matches(line[1:], groups)
    return s


def get_number_arrangements(line: str, groups: list[int], unfold: bool = False) -> int:
    if unfold:
        line = '?'.join(line for _ in range(5))
        groups *= 5
    return get_num_matches(line + '.', tuple(groups))


def part1(input_data: str):
    lines = [(line.split()[0], list(map(int, line.split()[1].split(',')))) for line in input_data.splitlines()]
    return sum(get_number_arrangements(*line) for line in lines)


def part2(input_data: str):
    lines = [(line.split()[0], list(map(int, line.split()[1].split(',')))) for line in input_data.splitlines()]
    return sum(get_number_arrangements(*line, unfold=True) for line in lines)


if __name__ == '__main__':
    assert get_number_arrangements('???.###', [1, 1, 3]) == 1
    assert get_number_arrangements('.??..??...?##.', [1, 1, 3]) == 4
    assert get_number_arrangements('?#?#?#?#?#?#?#?', [1, 3, 1, 6]) == 1
    assert get_number_arrangements('????.#...#...', [4, 1, 1]) == 1
    assert get_number_arrangements('????.######..#####.', [1, 6, 5]) == 4
    assert get_number_arrangements('???????', [2, 1]) == 10
    assert get_number_arrangements('?###????????', [3, 2, 1]) == 10
    assert part1(EXAMPLE) == 21
    assert get_number_arrangements('?????.???', [3, 2]) == 6
    assert get_number_arrangements('.#?#???????.????#', [1, 2, 3, 2, 1]) == 6
    assert part1(get_input()) == 7090
    print(f'Solution for part 1 is: {part1(get_input())}')

    assert get_number_arrangements('???.###', [1, 1, 3], unfold=True) == 1
    assert get_number_arrangements('.??..??...?##.', [1, 1, 3], unfold=True) == 16384
    assert get_number_arrangements('?#?#?#?#?#?#?#?', [1, 3, 1, 6], unfold=True) == 1
    assert get_number_arrangements('????.#...#...', [4, 1, 1], unfold=True) == 16
    assert get_number_arrangements('????.######..#####.', [1, 6, 5], unfold=True) == 2500
    assert get_number_arrangements('?###????????', [3, 2, 1], unfold=True) == 506250
    assert part2(EXAMPLE) == 525152
    print(f'Solution for part 2 is: {part2(get_input())}')
