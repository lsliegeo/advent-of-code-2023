import re

from util.input_util import get_input

EXAMPLE = """rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"""


def holiday_ascii_string_helper_algorithm(line: str) -> int:
    r = 0
    for c in line:
        r = ((r + ord(c)) * 17) % 256
    return r


def part1(input_data: str):
    return sum(holiday_ascii_string_helper_algorithm(line) for line in input_data.splitlines()[0].split(','))


def part2(input_data: str):
    # Thankfully python iterates over a dict in insertion order
    boxes: list[dict[str, int]] = [{} for _ in range(256)]

    for part in input_data.splitlines()[0].split(','):
        label, operation, focal_length = re.match('(.*)([-=])(\d*)', part).groups()
        box_nr = holiday_ascii_string_helper_algorithm(label)
        if operation == '=':
            boxes[box_nr][label] = int(focal_length)
        else:
            if label in boxes[box_nr]:
                del boxes[box_nr][label]

    return sum((box_nr + 1) * (slot_nr + 1) * focal_length for box_nr, box in enumerate(boxes) for slot_nr, focal_length in enumerate(box.values()))


if __name__ == '__main__':
    assert holiday_ascii_string_helper_algorithm('HASH') == 52
    assert part1(EXAMPLE) == 1320
    print(f'Solution for part 1 is: {part1(get_input())}')

    assert part2(EXAMPLE) == 145
    print(f'Solution for part 2 is: {part2(get_input())}')
