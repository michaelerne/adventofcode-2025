from run_util import run_puzzle
from typing import List

def parse_data(data) -> List[List[str]]:
    return [list(line.strip()) for line in data.strip().splitlines()]


def part_a(data):
    grid = parse_data(data)
    row_count = len(grid)
    column_count = len(grid[0])

    accessible_count = 0

    neighbor_deltas = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),           (0, 1),
        (1, -1),  (1, 0),  (1, 1),
    ]

    for row_index in range(row_count):
        for column_index in range(column_count):
            if grid[row_index][column_index] != '@':
                continue

            neighbor_rolls = 0
            for delta_row, delta_col in neighbor_deltas:
                neighbor_row = row_index + delta_row
                neighbor_col = column_index + delta_col
                if (
                    0 <= neighbor_row < row_count
                    and 0 <= neighbor_col < len(grid[neighbor_row])
                    and grid[neighbor_row][neighbor_col] == '@'
                ):
                    neighbor_rolls += 1

            if neighbor_rolls < 4:
                accessible_count += 1

    return accessible_count


def part_b(data):
    grid = parse_data(data)
    row_count = len(grid)
    column_count = len(grid[0])

    neighbor_deltas = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),           (0, 1),
        (1, -1),  (1, 0),  (1, 1),
    ]

    total_removed = 0

    while True:
        rolls_to_remove = []

        for row_index in range(row_count):
            for column_index in range(column_count):
                if grid[row_index][column_index] != '@':
                    continue

                neighbor_rolls = 0
                for delta_row, delta_col in neighbor_deltas:
                    neighbor_row = row_index + delta_row
                    neighbor_col = column_index + delta_col
                    if (
                        0 <= neighbor_row < row_count
                        and 0 <= neighbor_col < len(grid[neighbor_row])
                        and grid[neighbor_row][neighbor_col] == '@'
                    ):
                        neighbor_rolls += 1

                if neighbor_rolls < 4:
                    rolls_to_remove.append((row_index, column_index))

        if not rolls_to_remove:
            break

        for row_index, column_index in rolls_to_remove:
            grid[row_index][column_index] = '.'

        total_removed += len(rolls_to_remove)

    return total_removed


def main():
    examples = [
        (
            """..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@.
""",
            13,
            43,
        )
    ]
    day = int(__file__.split('/')[-1].split('.')[0][-2:])
    run_puzzle(day, part_a, part_b, examples)


if __name__ == '__main__':
    main()
