from util.input_util import get_input

EXAMPLE = """???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1"""


def get_number_arrangements(line: str, groups: list[int]) -> int:
    result = []
    branch_and_bound(line, groups, 0, 0, '', result)
    return len(set(result))


def branch_and_bound(line: str, groups: list[int], index: int, current_group_length: int, current_str: str, result: list[str]):
    if index >= len(line):
        if not groups or groups == [current_group_length]:
            result.append(current_str)
        return

    need_to_finish_group = groups and current_group_length == groups[0]
    need_to_continue_group = groups and 0 < current_group_length < groups[0]

    if need_to_finish_group:
        if line[index] == '#':
            return
        branch_and_bound(line, groups[1:], index + 1, 0, current_str + '.', result)

    elif need_to_continue_group:
        if line[index] == '.':
            return
        else:
            branch_and_bound(line, groups, index + 1, current_group_length + 1, current_str + '#', result)

    else:
        if groups:
            if line[index] != '.':
                branch_and_bound(line, groups, index + 1, 1, current_str + '#', result)
            if line[index] != '#':
                branch_and_bound(line, groups, index + 1, 0, current_str + '.', result)
        else:
            if line[index] != '#':
                branch_and_bound(line, groups, index + 1, 0, current_str + '.', result)


def part1(input_data: str):
    lines = [(line.split()[0], list(map(int, line.split()[1].split(',')))) for line in input_data.splitlines()]
    return sum(get_number_arrangements(*line) for line in lines)


def part2(input_data: str):
    pass


if __name__ == '__main__':
    assert get_number_arrangements('???.###', [1, 1, 3]) == 1
    assert get_number_arrangements('.??..??...?##.', [1, 1, 3]) == 4
    assert get_number_arrangements('?#?#?#?#?#?#?#?', [1, 3, 1, 6]) == 1
    assert get_number_arrangements('????.#...#...', [4, 1, 1]) == 1
    assert get_number_arrangements('????.######..#####.', [1, 6, 5]) == 4
    assert get_number_arrangements('?###????????', [3, 2, 1]) == 10
    assert part1(EXAMPLE) == 21
    print(f'Solution for part 1 is: {part1(get_input())}')

    assert part2(EXAMPLE) == None
    print(f'Solution for part 2 is: {part2(get_input())}')
