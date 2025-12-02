from run_util import run_puzzle


def parse_data(data):
    ranges = []
    for range_str in data.split(','):
        start, end = range_str.split('-')
        ranges.append((int(start), int(end)))

    return ranges


def is_valid_a(product_id):
    string = str(product_id)
    length = len(string)

    if string[0:length//2] == string[length//2:]:
        return False
    return True


def is_valid_b(product_id):
    string = str(product_id)
    length = len(string)

    for sub_length in range(1, length // 2 + 1):
        if length % sub_length != 0:
            continue
        substring = string[:sub_length]
        if substring * (length // sub_length) == string:
            return False
    return True


def part_a(data):
    data = parse_data(data)
    solution = 0
    for start, end in data:
        for product_id in range(start, end+1):
            if not is_valid_a(product_id):
                solution += product_id
    return solution


def part_b(data):
    data = parse_data(data)
    solution = 0
    for start, end in data:
        for product_id in range(start, end+1):
            if not is_valid_b(product_id):
                solution += product_id
    return solution


def main():
    examples = [
        ("""11-22,95-115,998-1012,1188511880-1188511890,222220-222224,
1698522-1698528,446443-446449,38593856-38593862,565653-565659,
824824821-824824827,2121212118-2121212124""", 1227775554, 4174379265)
    ]
    day = int(__file__.split('/')[-1].split('.')[0][-2:])
    run_puzzle(day, part_a, part_b, examples)


if __name__ == '__main__':
    main()