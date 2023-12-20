import re

from util.grid_utils import Coordinate, Direction
from util.input_util import get_input

EXAMPLE = """R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)"""

CHAR_TO_DIRECTION = {
    'R': Direction.EAST,
    'D': Direction.SOUTH,
    'L': Direction.WEST,
    'U': Direction.NORTH,
}

INT_TO_DIRECTION = {
    '0': Direction.EAST,
    '1': Direction.SOUTH,
    '2': Direction.WEST,
    '3': Direction.NORTH,
}


def intersect(co_a: tuple[Coordinate, Coordinate], co_b: tuple[Coordinate, Coordinate]) -> bool:
    a_horizontal = co_a[0].x == co_a[1].x
    b_horizontal = co_b[0].x == co_b[1].x

    if a_horizontal:
        if co_a[0].y > co_a[1].y:
            co_a = co_a[::-1]
    else:
        if co_a[0].x > co_a[1].x:
            co_a = co_a[::-1]
    if b_horizontal:
        if co_b[0].y > co_b[1].y:
            co_b = co_b[::-1]
    else:
        if co_b[0].x > co_b[1].x:
            co_b = co_b[::-1]

    match a_horizontal, b_horizontal:
        case True, True:
            if co_a[0].y > co_b[0].y:
                co_a, co_b = co_b, co_a
            return co_a[0].x == co_b[0].x and co_a[0].y < co_b[0].y < co_a[1].y
        case False, False:
            if co_a[0].x > co_b[0].x:
                co_a, co_b = co_b, co_a
            return co_a[0].y == co_b[0].y and co_a[0].x < co_b[0].x < co_a[1].x
        case True, False:
            return co_a[0].y <= co_b[0].y <= co_a[1].y and co_b[0].x <= co_a[1].x <= co_b[1].x
        case False, True:
            return co_b[0].y <= co_a[0].y <= co_b[1].y and co_a[0].x <= co_b[1].x <= co_a[1].x


assert intersect((Coordinate(0, 3), Coordinate(0, 6)), (Coordinate(0, 0), Coordinate(0, 10)))
assert intersect((Coordinate(0, 3), Coordinate(0, 6)), (Coordinate(0, 4), Coordinate(0, 10)))
assert not intersect((Coordinate(0, 3), Coordinate(0, 6)), (Coordinate(0, 7), Coordinate(0, 10)))
assert not intersect((Coordinate(0, 3), Coordinate(0, 6)), (Coordinate(-2, 0), Coordinate(2, 0)))
assert intersect((Coordinate(0, 3), Coordinate(0, 6)), (Coordinate(-2, 4), Coordinate(2, 4)))
assert intersect((Coordinate(0, 0), Coordinate(0, 10)), (Coordinate(-5, 10), Coordinate(5, 10)))
assert not intersect((Coordinate(0, 0), Coordinate(0, 10)), (Coordinate(4, 1), Coordinate(4, 9)))
assert not intersect((Coordinate(8, 1), Coordinate(1, 1)), (Coordinate(2, 2), Coordinate(5, 2)))
assert intersect((Coordinate(8, 1), Coordinate(1, 1)), (Coordinate(2, 0), Coordinate(2, 2)))


def any_intersects_with(corners: list[Coordinate], co_a: Coordinate, co_b: Coordinate) -> bool:
    if abs(co_a.x - co_b.x) == 1 or abs(co_a.y - co_b.y) == 1:
        return False
    return any(
        # StraightLine.intersect(StraightLine(co_a, co_b), StraightLine(corners[i], corners[(i + 1) % len(corners)]))
        intersect((co_a, co_b), (corners[i], corners[(i + 1) % len(corners)]))
        for i in range(len(corners))
    )


def trim_once(corners: list[Coordinate], reverse: bool) -> int | None:
    trimmed_area = None
    if reverse:
        corners.reverse()

    for i in range(len(corners)):
        a = corners[i % len(corners)]
        b = corners[(i + 1) % len(corners)]
        c = corners[(i + 2) % len(corners)]
        d = corners[(i + 3) % len(corners)]

        if a.x < d.x and d.y < a.y < b.y:
            """
              a#####b
                    #
            d#*#####c
            """
            new_point = Coordinate(d.x, a.y)
            if not any_intersects_with(corners, a.step(Direction.SOUTH), new_point.step(Direction.NORTH)):
                trimmed_area = (c.x - b.x + 1) * (b.y - a.y)
                for _ in range(3):
                    corners.pop(i if i < len(corners) else 0)
                corners.insert(i if i < len(corners) else 0, new_point)
        elif a.x < d.x and a.y < d.y < b.y:
            """
            a#*#####b
                    #
              d#####c
            """
            new_point = Coordinate(a.x, d.y)
            if not any_intersects_with(corners, d.step(Direction.NORTH), new_point.step(Direction.SOUTH)):
                trimmed_area = (c.x - b.x + 1) * (c.y - d.y)
                for _ in range(3):
                    corners.pop(i + 1 if i + 1 < len(corners) else 0)
                corners.insert(i + 1 if i + 1 < len(corners) else 0, new_point)
        elif a.y == d.y and a.x < d.x and a.x < d.x and a.y < b.y:
            """
            a#######b
                    #
            d#######c
            """
            if not any_intersects_with(corners, a.step(Direction.SOUTH), d.step(Direction.NORTH)):
                trimmed_area = (c.x - b.x + 1) * (b.y - a.y)
                for _ in range(4):
                    corners.pop(i if i < len(corners) else 0)
        elif a.y < d.y and b.x < d.x < a.x:
            """
            b###c
            #   #
            *   d
            #
            a
            """
            new_point = Coordinate(d.x, a.y)
            if not any_intersects_with(corners, new_point.step(Direction.EAST), d.step(Direction.WEST)):
                trimmed_area = (c.y - b.y + 1) * (d.x - c.x)
                for _ in range(3):
                    corners.pop(i + 1 if i + 1 < len(corners) else 0)
                corners.insert(i + 1 if i + 1 < len(corners) else 0, new_point)
        elif a.y < d.y and b.x < a.x < d.x:
            """
            b###c
            #   #
            a   *
                #
                d
            """
            new_point = Coordinate(a.x, d.y)
            if not any_intersects_with(corners, a.step(Direction.EAST), new_point.step(Direction.WEST)):
                trimmed_area = (c.y - b.y + 1) * (a.x - b.x)
                for _ in range(3):
                    corners.pop(i if i < len(corners) else 0)
                corners.insert(i if i < len(corners) else 0, new_point)
        elif a.x == d.x and a.y < d.y and a.x > b.x and d.y > a.y:
            """
            b###c
            #   #
            #   #
            a   d
            """
            if not any_intersects_with(corners, a.step(Direction.EAST), d.step(Direction.WEST)):
                trimmed_area = (c.y - b.y + 1) * (a.x - b.x)
                for _ in range(4):
                    corners.pop(i if i < len(corners) else 0)
        elif d.x < a.x and c.y < a.y < d.y:
            """
            c#####*#d
            #
            b#####a
            """
            new_point = Coordinate(d.x, a.y)
            if not any_intersects_with(corners, a.step(Direction.NORTH), new_point.step(Direction.SOUTH)):
                trimmed_area = (b.x - c.x + 1) * (a.y - b.y)
                for _ in range(3):
                    corners.pop(i if i < len(corners) else 0)
                corners.insert(i if i < len(corners) else 0, new_point)
        elif d.x < a.x and c.y < d.y < a.y:
            """
            c#####d
            #
            b#####*#a
            """
            new_point = Coordinate(a.x, d.y)
            if not any_intersects_with(corners, new_point.step(Direction.NORTH), d.step(Direction.SOUTH)):
                trimmed_area = (b.x - c.x + 1) * (d.y - c.y)
                for _ in range(3):
                    corners.pop(i + 1 if i + 1 < len(corners) else 0)
                corners.insert(i + 1 if i + 1 < len(corners) else 0, new_point)
        elif d.y == a.y and d.x < a.x and c.y < d.y and b.y < a.y:
            """
            c#####d
            #
            b#####a
            """
            if not any_intersects_with(corners, a.step(Direction.SOUTH), d.step(Direction.NORTH)):
                trimmed_area = (b.x - c.x + 1) * (d.y - c.y)
                for _ in range(4):
                    corners.pop(i if i < len(corners) else 0)
        elif d.y < a.y and c.x > a.x > d.x:
            """
            d
            #
            *   a
            #   #
            c###b
            """
            new_point = Coordinate(a.x, d.y)
            if not any_intersects_with(corners, new_point.step(Direction.EAST), a.step(Direction.WEST)):
                trimmed_area = (b.y - c.y + 1) * (b.x - a.x)
                for _ in range(3):
                    corners.pop(i if i < len(corners) else 0)
                corners.insert(i if i < len(corners) else 0, new_point)
        elif d.y < a.y and c.x > d.x > a.x:
            """
                a
                #
            d   *
            #   #
            c###b
            """
            new_point = Coordinate(d.x, a.y)
            if not any_intersects_with(corners, d.step(Direction.EAST), new_point.step(Direction.WEST)):
                trimmed_area = (b.y - c.y + 1) * (c.x - d.x)
                for _ in range(3):
                    corners.pop(i + 1 if i + 1 < len(corners) else 0)
                corners.insert(i + 1 if i + 1 < len(corners) else 0, new_point)
        elif d.x == a.x and d.y < a.y and d.x < c.x and a.x < b.x:
            """
            d   a
            #   #
            #   #
            #   #
            c###b
            """
            if not any_intersects_with(corners, d.step(Direction.EAST), a.step(Direction.WEST)):
                trimmed_area = (b.y - c.y + 1) * (c.x - d.x)
                for _ in range(4):
                    corners.pop(i if i < len(corners) else 0)

        if trimmed_area is not None:
            if reverse:
                corners.reverse()
                return -trimmed_area
            return trimmed_area

    if reverse:
        corners.reverse()
    assert trimmed_area is None or trimmed_area > 0
    if trimmed_area is not None and reverse:
        return -trimmed_area
    return trimmed_area


def calculate_volume(corners: list[Coordinate]) -> int:
    trimmed_area = 0
    while len(corners) > 4:
        trim_result = trim_once(corners, False)
        if trim_result is None:
            trim_result = trim_once(corners, True)
        if trim_result is None:
            break
        else:
            trimmed_area += trim_result

    if corners[0].x == corners[1].x:
        trimmed_area += (abs(corners[0].y - corners[1].y) + 1) * (abs(corners[1].x - corners[2].x) + 1)
    else:
        trimmed_area += (abs(corners[0].x - corners[1].x) + 1) * (abs(corners[1].y - corners[2].y) + 1)

    return trimmed_area


def part1(input_data: str, use_shoelace: bool = False):
    corners: list[Coordinate] = []
    co = Coordinate(0, 0)
    border_length = 0
    for line in input_data.splitlines():
        corners.append(co)
        char, amount, color = re.match('(.) (\d*) \((.*)\)', line).groups()
        border_length += int(amount)
        direction = CHAR_TO_DIRECTION[char]
        next_co = co.step(direction, int(amount))
        co = next_co

    if use_shoelace:
        return shoelace(corners, border_length)
    else:
        return calculate_volume(corners)


def part2(input_data: str, use_shoelace: bool = False):
    corners: list[Coordinate] = []
    co = Coordinate(0, 0)
    border_length = 0
    for line in input_data.splitlines():
        corners.append(co)
        amount_str, direction_int = re.search('#(.{5})(.)', line).groups()
        amount = int(amount_str, 16)
        border_length += amount
        direction = INT_TO_DIRECTION[direction_int]
        next_co = co.step(direction, amount)
        co = next_co

    if use_shoelace:
        return shoelace(corners, border_length)
    else:
        return calculate_volume(corners)


def shoelace(corners: list[Coordinate], border_length: int) -> int:
    result = 0
    for i in range(len(corners)):
        result += corners[i].x * (corners[(i + 1) % len(corners)].y - corners[(i - 1) % len(corners)].y) / 2
    return int(abs(result) + border_length / 2 + 1)


if __name__ == '__main__':
    assert part1(EXAMPLE) == 62
    assert part1(EXAMPLE, use_shoelace=True) == 62
    print(f'Solution for part 1 is: {part1(get_input())}')
    print(f'Solution for part 1 is: {part1(get_input(), use_shoelace=True)} (shoelace)')

    assert part2(EXAMPLE) == 952408144115
    assert part2(EXAMPLE, use_shoelace=True) == 952408144115
    print(f'Solution for part 2 is: {part2(get_input())}')
    print(f'Solution for part 2 is: {part2(get_input(), use_shoelace=True)} (shoelace)')
