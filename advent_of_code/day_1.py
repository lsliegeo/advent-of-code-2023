from typing import Iterator

from util.input_util import get_input

EXAMPLE = """1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet"""

EXAMPLE2 = """two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen"""


def part1(input_data: str):
    chars_to_look_for = '0123456789'
    result = 0
    for line in input_data.splitlines():
        first_match = None
        for char in line:
            if char in chars_to_look_for:
                first_match = char
                break
        last_match = None
        for char in reversed(line):
            if char in chars_to_look_for:
                last_match = char
                break
        result += int(first_match + last_match)
    return result


def suffixes(string: str, reverse: bool = False) -> Iterator[str]:
    """Returns an iterator of the suffixes of the input string. Ordered from the full string to the final char. Optional argument to iterate in reverse order."""
    if reverse:
        for i in reversed(range(len(string))):
            yield string[i:]
    else:
        for i in range(len(string)):
            yield string[i:]


def part2(input_data: str):
    digit_mapping = {
        'one': '1',
        'two': '2',
        'three': '3',
        'four': '4',
        'five': '5',
        'six': '6',
        'seven': '7',
        'eight': '8',
        'nine': '9',
    }
    strings_to_look_for = list('0123456789') + list(digit_mapping)

    def get_first_match(line: str, reverse: bool) -> str:
        """Get the first occurrence of any string in the digit mapping, and convert it to a (string representation of a) digit."""
        for suffix in suffixes(line, reverse=reverse):
            for string_to_look_for in strings_to_look_for:
                if suffix.startswith(string_to_look_for):
                    return digit_mapping.get(string_to_look_for, string_to_look_for)

    return sum(int(get_first_match(line, reverse=False) + get_first_match(line, reverse=True)) for line in input_data.splitlines())


if __name__ == '__main__':
    assert part1(EXAMPLE) == 142
    print(f'Solution for part 1 is: {part1(get_input())}')

    assert part2(EXAMPLE2) == 281
    print(f'Solution for part 2 is: {part2(get_input())}')
