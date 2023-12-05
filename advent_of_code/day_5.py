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
    parts = input_data.split('\n\n')
    seed_ints = list(map(int, parts[0][7:].split()))
    seeds: list[tuple[int, int]] = [(seed_ints[i], seed_ints[i + 1]) for i in range(0, len(seed_ints), 2)]
    mappings: list[list[tuple[int, int, int]]] = [parse_single_mapping(part) for part in parts[1:]]

    current_values: set[tuple[int, int]] = set(seeds)
    for mapping in mappings:
        next_values = set()
        for current_start, current_length in current_values:

            # We'll have to split the ranges
            # E.g. 123, 46 could result in multiple ranges after the mapping
            #   * 123, 34
            #   * 98, 4
            #   * 97489, 8
            while current_length > 0:

                possible_fits = [
                    (destination_start, source_start, source_length)
                    for destination_start, source_start, source_length in mapping
                    if source_start + source_length > current_start
                ]
                if not possible_fits:
                    # there is no range at all that fits, so use the 1on1 mapping
                    next_values.add((current_start, current_length))
                    break

                destination_start, source_start, source_length = min(possible_fits, key=lambda t: t[1])
                if source_start > current_start:
                    # the first range starts later that the current range. So we need to insert a 1on1 filler mapping
                    filler_range_length = source_start - current_start
                    if filler_range_length > current_length:
                        # the first range starts way too far away, more than we're looking for to match with
                        # after inserting the filler, we'll have handled the whole range before we arrive at this first matching range
                        next_values.add((current_start, current_length))
                        break
                    # insert filler to arrive at this first range
                    next_values.add((current_start, filler_range_length))
                    current_start += filler_range_length
                    current_length -= filler_range_length
                else:
                    # map the current range to the matching range
                    overlap_with_range = min(current_start + current_length, source_start + source_length) - current_start
                    next_values.add((current_start - source_start + destination_start, overlap_with_range))
                    current_start += overlap_with_range
                    current_length -= overlap_with_range

        current_values = next_values

    return min(range_start for range_start, range_length in current_values)


if __name__ == '__main__':
    assert part1(EXAMPLE) == 35
    print(f'Solution for part 1 is: {part1(get_input())}')

    assert part2(EXAMPLE) == 46
    print(f'Solution for part 2 is: {part2(get_input())}')
