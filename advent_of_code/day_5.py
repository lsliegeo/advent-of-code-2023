from util.input_util import get_input

EXAMPLE = """seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4"""


def parse_single_mapping(lines: str) -> list[tuple[int, int, int]]:
    return [
        tuple(map(int, line.split()))
        for line in lines.splitlines()[1:]
    ]


def part1(input_data: str):
    parts = input_data.split('\n\n')
    seeds = list(map(int, parts[0][7:].split()))
    mappings: list[list[tuple[int, int, int]]] = [parse_single_mapping(part) for part in parts[1:]]

    current_values = set(seeds)
    for mapping in mappings:
        next_values = set()
        for value in current_values:
            found = False
            for destination_start, source_start, number in mapping:
                if source_start <= value <= source_start + number:
                    next_values.add(value - source_start + destination_start)
                    found = True
                    break
            if not found:
                next_values.add(value)

        current_values = next_values

    return min(current_values)


def part2(input_data: str):
    pass


if __name__ == '__main__':
    assert part1(EXAMPLE) == 35
    print(f'Solution for part 1 is: {part1(get_input())}')

    assert part2(EXAMPLE) == None
    print(f'Solution for part 2 is: {part2(get_input())}')
