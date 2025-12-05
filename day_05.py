import bisect

from run_util import run_puzzle


def merge_ranges(ranges):
    merged = []
    for start, end in sorted(ranges):
        if not merged or start > merged[-1][1] + 1:
            merged.append([start, end])
        else:
            merged[-1][1] = max(merged[-1][1], end)
    return merged


def parse_data(data):
    ranges_block, ids_block = data.strip().split("\n\n")

    ranges = [
        list(map(int, line.strip().split("-")))
        for line in ranges_block.strip().splitlines()
    ]
    merged_ranges = merge_ranges(ranges)

    ingredient_ids = [
        int(line)
        for line in ids_block.strip().splitlines()
    ]

    return merged_ranges, ingredient_ids


def part_a(data):
    merged_ranges, ingredient_ids = parse_data(data)

    starts = [start for start, _ in merged_ranges]

    return sum(
        1
        for value in ingredient_ids
        if (index := bisect.bisect_right(starts, value) - 1) >= 0
        and merged_ranges[index][0] <= value <= merged_ranges[index][1]
    )


def part_b(data):
    merged_ranges, _ = parse_data(data)

    return sum(
        end - start + 1
        for start, end in merged_ranges
    )


def main():
    examples = [
        (
            """3-5
10-14
16-20
12-18

1
5
8
11
17
32
""",
            3,
            14,
        )
    ]
    day = int(__file__.split('/')[-1].split('.')[0][-2:])
    run_puzzle(day, part_a, part_b, examples)


if __name__ == '__main__':
    main()
