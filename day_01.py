from run_util import run_puzzle
from operator import add, sub
from typing import Callable, List, Tuple

def parse_data(data) -> List[Tuple[str, Callable[[int, int], int], int]]:
    return [
        (line[0], add if line[0] == 'R' else sub, int(line[1:]))
        for line in data.strip().splitlines()
    ]


def part_a(data):
    data = parse_data(data)
    dial = 50

    zeros = 0
    for _direction, operation, steps in data:
        dial = operation(dial, steps) % 100

        if dial == 0:
            zeros += 1
    return zeros


def part_b(data):
    data = parse_data(data)
    dial = 50
    zeros = 0

    for direction, operation, steps in data:

        new_position = operation(dial, steps) % 100
        zeros += steps // 100

        if direction == 'R':
            if new_position < dial:
                zeros += 1
        else:  # direction == 'L':
            if dial != 0 and (new_position > dial or new_position == 0):
                zeros += 1

        dial = new_position

    return zeros

def main():
    examples = [
        ("""L68
L30
R48
L5
R60
L55
L1
L99
R14
L82
""", 3, 6)
    ]
    day = int(__file__.split('/')[-1].split('.')[0][-2:])
    run_puzzle(day, part_a, part_b, examples)


if __name__ == '__main__':
    main()