from collections import deque
from functools import lru_cache

from run_util import run_puzzle


def parse_data(data):
    data = data.strip("\n")
    grid = data.splitlines()

    number_of_rows = len(grid)
    number_of_columns = len(grid[0])

    start_row, start_column = find_start(grid)

    return grid, number_of_rows, number_of_columns, start_row, start_column


def find_start(grid):
    for row_index, row in enumerate(grid):
        for column_index, char in enumerate(row):
            if char == "S":
                return row_index, column_index
    return None, None


def part_a(data):
    grid, number_of_rows, number_of_columns, start_row, start_column = parse_data(data)

    visited = set()
    queue = deque()

    visited.add((start_row, start_column))
    queue.append((start_row, start_column))

    split_count = 0

    while queue:
        row_index, column_index = queue.popleft()
        cell = grid[row_index][column_index]

        if cell == "^":
            split_count += 1
            next_positions = [
                (row_index + 1, column_index - 1),
                (row_index + 1, column_index + 1),
            ]
        else:
            next_positions = [
                (row_index + 1, column_index),
            ]

        for next_row, next_column in next_positions:
            if 0 <= next_row < number_of_rows and 0 <= next_column < number_of_columns:
                if (next_row, next_column) not in visited:
                    visited.add((next_row, next_column))
                    queue.append((next_row, next_column))

    return split_count


def part_b(data):
    grid, number_of_rows, number_of_columns, start_row, start_column = parse_data(data)

    @lru_cache(maxsize=None)
    def count_paths(row_index, column_index):
        cell = grid[row_index][column_index]

        if cell == "^":
            total_paths = 0
            for delta_column in (-1, 1):
                next_row = row_index + 1
                next_column = column_index + delta_column

                if 0 <= next_row < number_of_rows and 0 <= next_column < number_of_columns:
                    total_paths += count_paths(next_row, next_column)
                else:
                    total_paths += 1
            return total_paths
        else:
            next_row = row_index + 1
            next_column = column_index

            if 0 <= next_row < number_of_rows:
                return count_paths(next_row, next_column)
            else:
                return 1

    return count_paths(start_row, start_column)


def main():
    examples = [
        (
            """.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
...............
""",
            21,
            40,
        )
    ]
    day = int(__file__.split('/')[-1].split('.')[0][-2:])
    run_puzzle(day, part_a, part_b, examples)


if __name__ == '__main__':
    main()
