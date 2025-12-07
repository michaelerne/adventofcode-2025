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

    reachable_current = [False] * number_of_columns
    reachable_current[start_column] = True

    split_count = 0

    for row_index in range(start_row, number_of_rows):
        row = grid[row_index]
        reachable_next = [False] * number_of_columns

        for column_index in range(number_of_columns):
            if not reachable_current[column_index]:
                continue

            cell = row[column_index]
            if cell == "^":
                split_count += 1
                next_row = row_index + 1
                if next_row < number_of_rows:
                    left_column = column_index - 1
                    right_column = column_index + 1
                    if left_column >= 0:
                        reachable_next[left_column] = True
                    if right_column < number_of_columns:
                        reachable_next[right_column] = True
            else:
                next_row = row_index + 1
                if next_row < number_of_rows:
                    reachable_next[column_index] = True

        reachable_current = reachable_next

    return split_count


def part_b(data):
    grid, number_of_rows, number_of_columns, start_row, start_column = parse_data(data)

    paths_next = [0] * number_of_columns
    paths_current = [0] * number_of_columns

    bottom_row = number_of_rows - 1
    row = grid[bottom_row]
    for col in range(number_of_columns):
        cell = row[col]
        if cell == "^":
            total_paths = 0
            for delta in (-1, 1):
                next_col = col + delta
                if 0 <= next_col < number_of_columns:
                    total_paths += 1
                else:
                    total_paths += 1
            paths_next[col] = total_paths
        else:
            paths_next[col] = 1

    for row_index in range(number_of_rows - 2, -1, -1):
        row = grid[row_index]
        for col in range(number_of_columns):
            cell = row[col]
            if cell == "^":
                total_paths = 0
                for delta in (-1, 1):
                    next_col = col + delta
                    if 0 <= next_col < number_of_columns:
                        total_paths += paths_next[next_col]
                    else:
                        total_paths += 1
                paths_current[col] = total_paths
            else:
                paths_current[col] = paths_next[col]

        paths_next, paths_current = paths_current, paths_next

    return paths_next[start_column]


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
