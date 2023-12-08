from typing import Iterator

from util.input_util import get_input

EXAMPLE = """RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)"""

EXAMPLE2 = """LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)"""


def part1(input_data: str):
    network: dict[str, tuple[str, str]] = {
        line.split(' = ')[0]: tuple(line.split(' = ')[1].strip('(').strip(')').split(', '))
        for line in input_data.splitlines()[2:]
    }

    def steps_iterator() -> Iterator[bool]:
        s = [c == 'R' for c in input_data.splitlines()[0]]
        while 1:
            yield from s

    number_steps = 0
    current = 'AAA'
    steps = steps_iterator()
    while current != 'ZZZ':
        current = network[current][next(steps)]
        number_steps += 1
    return number_steps


def part2(input_data: str):
    pass


if __name__ == '__main__':
    assert part1(EXAMPLE) == 2
    assert part1(EXAMPLE2) == 6
    print(f'Solution for part 1 is: {part1(get_input())}')

    assert part2(EXAMPLE) == None
    print(f'Solution for part 2 is: {part2(get_input())}')
