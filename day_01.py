from run_util import run_puzzle
from operator import add, sub

def parse_data(data):
    return [
        (line[0], int(line[1:]))
        for line in data.strip().splitlines()
    ]


def part_a(data):
    data = parse_data(data)
    dial = 50
    zeros = 0
    for direction, steps in data:
        if direction == 'R':
            dial += steps
        else:
            dial -= steps

        if dial < 0:
            dial += 100
        dial %= 100

        if dial == 0:
            zeros += 1

    return zeros


def part_b(data):
    data = parse_data(data)
    dial = 50
    positions = []

    for direction, steps in data:
        if direction == 'R':
            for _ in range(steps):
                dial = (dial + 1) % 100
                positions.append(dial)
        else:
            for _ in range(steps):
                dial = (dial - 1) % 100
                positions.append(dial)
    return sum(1 for position in positions if position == 0)

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