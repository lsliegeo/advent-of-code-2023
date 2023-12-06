import math

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
    duration = int(input_data.splitlines()[0].split(':')[1].replace(' ', ''))
    distance_to_beat = int(input_data.splitlines()[1].split(':')[1].replace(' ', ''))

    result = 0
    for i in range(1, duration):
        if i * (duration - i) > distance_to_beat:
            result += 1

    return result


def part2_mathematical(input_data: str):
    duration = int(input_data.splitlines()[0].split(':')[1].replace(' ', ''))
    distance_to_beat = int(input_data.splitlines()[1].split(':')[1].replace(' ', ''))

    # f(x) = -x ** 2 + duration * x - distance_to_beat
    # f(x) = a * x**2 + b * x + c
    a = -1
    b = duration
    c = -distance_to_beat
    discriminant = duration ** 2 - 4 * a * c
    if discriminant <= 0:
        raise ValueError('Unexpected discriminant')
    x1 = (-b - math.sqrt(discriminant)) / (2 * a)
    x2 = (-b + math.sqrt(discriminant)) / (2 * a)

    x_min = min(x1, x2)
    x_max = max(x1, x2)

    return int(x_max) - int(x_min)


if __name__ == '__main__':
    assert part1(EXAMPLE) == 288
    print(f'Solution for part 1 is: {part1(get_input())}')

    assert part2_mathematical(EXAMPLE) == 71503
    print(f'Solution for part 2 is: {part2_mathematical(get_input())}')

    assert part2(EXAMPLE) == 71503
    # takes ~13 sec
    print(f'Solution for part 2 is: {part2(get_input())}')
