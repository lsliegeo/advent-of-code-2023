from util.input_util import get_input

EXAMPLE = """rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"""


def HASH(line: str) -> int:
    r = 0
    for c in line:
        r = ((r + ord(c)) * 17) % 256
    return r


def part1(input_data: str):
    return sum(HASH(line) for line in input_data.splitlines()[0].split(','))


def part2(input_data: str):
    pass


if __name__ == '__main__':
    assert HASH('HASH') == 52
    assert part1(EXAMPLE) == 1320
    print(f'Solution for part 1 is: {part1(get_input())}')

    assert part2(EXAMPLE) == None
    print(f'Solution for part 2 is: {part2(get_input())}')
