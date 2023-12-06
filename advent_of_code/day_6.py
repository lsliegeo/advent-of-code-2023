from util.input_util import get_input

EXAMPLE = """Time:      7  15   30
Distance:  9  40  200"""


def part1(input_data: str):
    duration_to_distance_to_beat = dict(zip(map(int, input_data.splitlines()[0].split(':')[1].split()), map(int, input_data.splitlines()[1].split(':')[1].split())))

    result = 1
    for duration, distance_to_beat in duration_to_distance_to_beat.items():
        button_press_duration_to_distance = {i: i * (duration - i) for i in range(1, duration)}
        result *= sum(distance > distance_to_beat for distance in button_press_duration_to_distance.values())

    return result


def part2(input_data: str):
    pass


if __name__ == '__main__':
    assert part1(EXAMPLE) == 288
    print(f'Solution for part 1 is: {part1(get_input())}')

    assert part2(EXAMPLE) == None
    print(f'Solution for part 2 is: {part2(get_input())}')
