from run_util import run_puzzle


def parse_data(data: str):
    return [
        line.strip()
        for line in data.splitlines()
    ]


def get_max_joltage(bank: str, batteries_to_take: int) -> int:
    bank_length = len(bank)

    result_digits = []
    start = 0
    remaining = batteries_to_take

    while remaining > 0:
        end = bank_length - remaining
        max_digit = '-1'
        max_idx = start
        for idx in range(start, end + 1):
            if bank[idx] > max_digit:
                max_digit = bank[idx]
                max_idx = idx
                if max_digit == '9':
                    break
        result_digits.append(max_digit)
        start = max_idx + 1
        remaining -= 1

    return int("".join(result_digits))


def part_a(data):
    banks = parse_data(data)
    take = 2
    return sum(get_max_joltage(bank, take) for bank in banks)


def part_b(data):
    banks = parse_data(data)
    take = 12
    return sum(get_max_joltage(bank, take) for bank in banks)


def main():
    example_input = (
        "987654321111111\n"
        "811111111111119\n"
        "234234234234278\n"
        "818181911112111\n"
    )
    examples = [
        (example_input, 357, 3121910778619),
    ]
    day = int(__file__.split('/')[-1].split('.')[0][-2:])
    run_puzzle(day, part_a, part_b, examples)


if __name__ == '__main__':
    main()
