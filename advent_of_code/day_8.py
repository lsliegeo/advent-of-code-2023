import math
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

EXAMPLE3 = """LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)"""


def steps_iterator(steps_str: str) -> Iterator[bool]:
    s = [c == 'R' for c in steps_str.splitlines()[0]]
    while 1:
        yield from s


def parse_network(input_data: str) -> dict[str, tuple[str, str]]:
    return {
        line.split(' = ')[0]: tuple(line.split(' = ')[1][1:-1].split(', '))
        for line in input_data.splitlines()[2:]
    }


def steps_until_end(network: dict[str, tuple[str, str]], steps_str: str, current: str, until_zzz: bool) -> int:
    number_steps = 0
    steps = steps_iterator(steps_str)
    while current != 'ZZZ' if until_zzz else current[-1] != 'Z':
        current = network[current][next(steps)]
        number_steps += 1
    return number_steps


def part1(input_data: str):
    network = parse_network(input_data)
    return steps_until_end(network, input_data.splitlines()[0], 'AAA', until_zzz=True)


def part2(input_data: str):
    network = parse_network(input_data)
    return math.lcm(*[steps_until_end(network, input_data.splitlines()[0], pos, until_zzz=False) for pos in network if pos[-1] == 'A'])


if __name__ == '__main__':
    assert part1(EXAMPLE) == 2
    assert part1(EXAMPLE2) == 6
    print(f'Solution for part 1 is: {part1(get_input())}')

    assert part2(EXAMPLE3) == 6
    print(f'Solution for part 2 is: {part2(get_input())}')
