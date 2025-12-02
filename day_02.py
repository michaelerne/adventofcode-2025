from typing import List, Tuple, Set

from run_util import run_puzzle


def parse_data(data: str) -> List[Tuple[int, int]]:
    ranges: List[Tuple[int, int]] = []
    for range_spec in data.split(','):
        start_str, end_str = range_spec.split('-')
        ranges.append((int(start_str), int(end_str)))
    return sorted(ranges)


def generate_invalid_ids_upto(max_value: int, half_only: bool) -> List[int]:
    invalid_ids: Set[int] = set()
    max_digits = len(str(max_value))

    max_block_digits = max_digits // 2 if half_only else max_digits - 1

    for block_digits in range(1, max_block_digits + 1):
        if half_only:
            repetition_counts = (2,)
        else:
            max_repetitions = max_digits // block_digits
            if max_repetitions < 2:
                continue
            repetition_counts = range(2, max_repetitions + 1)

        block_shift = 10 ** block_digits

        for repeat_count in repetition_counts:
            total_digits = block_digits * repeat_count

            multiplier = (block_shift ** repeat_count - 1) // (block_shift - 1)

            block_start = 10 ** (block_digits - 1)
            block_end_full = 10 ** block_digits - 1

            if total_digits < max_digits:
                block_end = block_end_full
            else:
                block_end = min(block_end_full, max_value // multiplier)
                if block_end < block_start:
                    continue

            for block in range(block_start, block_end + 1):
                invalid_ids.add(block * multiplier)

    return sorted(invalid_ids)


def invalid_ids_in_ranges(ranges: List[Tuple[int, int]], half_only: bool = False, ) -> List[int]:
    max_value = max(end for _, end in ranges)
    invalid_ids = generate_invalid_ids_upto(max_value, half_only)

    covered_invalid_ids: List[int] = []
    range_index = 0

    for invalid_id in invalid_ids:
        while range_index < len(ranges) and invalid_id > ranges[range_index][1]:
            range_index += 1
        if range_index == len(ranges):
            break
        if ranges[range_index][0] <= invalid_id <= ranges[range_index][1]:
            covered_invalid_ids.append(invalid_id)

    return covered_invalid_ids


def part_a(data: str) -> int:
    ranges = parse_data(data)
    return sum(invalid_ids_in_ranges(ranges, half_only=True))


def part_b(data: str) -> int:
    ranges = parse_data(data)
    return sum(invalid_ids_in_ranges(ranges))


def main() -> None:
    examples = [
        ("""11-22,95-115,998-1012,1188511880-1188511890,222220-222224,
1698522-1698528,446443-446449,38593856-38593862,565653-565659,
824824821-824824827,2121212118-2121212124""", 1227775554, 4174379265)
    ]
    day = int(__file__.split('/')[-1].split('.')[0][-2:])
    run_puzzle(day, part_a, part_b, examples)


if __name__ == '__main__':
    main()
