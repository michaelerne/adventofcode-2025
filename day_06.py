from run_util import run_puzzle


def parse_data(data):
    grid = [line.rstrip("\n") for line in data.strip("\n").split("\n")]

    number_of_rows = len(grid)
    number_of_columns = len(grid[0])

    problem_ranges = []
    current_start = None

    for column_index in range(number_of_columns):
        is_empty = True
        for row_index in range(number_of_rows):
            if grid[row_index][column_index] != " ":
                is_empty = False
                break

        if is_empty:
            if current_start is not None:
                problem_ranges.append((current_start, column_index))
                current_start = None
        else:
            if current_start is None:
                current_start = column_index

    if current_start is not None:
        problem_ranges.append((current_start, number_of_columns))

    return grid, problem_ranges


def part_a(data):
    grid, problem_ranges = parse_data(data)
    number_of_rows = len(grid)
    bottom_row_index = number_of_rows - 1

    grand_total = 0

    for start_column, end_column in problem_ranges:
        bottom_slice = grid[bottom_row_index][start_column:end_column]
        operator_char = next(char for char in bottom_slice if char in "+*")

        numbers = [
            int(row[start_column:end_column])
            for row in grid[:bottom_row_index]
        ]

        if operator_char == '+':
            value = sum(numbers)
        else:
            value = 1
            for number in numbers:
                value *= number

        grand_total += value

    return grand_total


def part_b(data):
    grid, problem_ranges = parse_data(data)
    number_of_rows = len(grid)
    bottom_row_index = number_of_rows - 1

    grand_total = 0

    for start_column, end_column in problem_ranges:
        bottom_slice = grid[bottom_row_index][start_column:end_column]
        operator_char = next(char for char in bottom_slice if char in "+*")

        numbers = [
            int("".join(
                [
                    grid[row_index][column_index]
                    for row_index in range(bottom_row_index)
                    if grid[row_index][column_index].isdigit()
                ]
            ))
            for column_index in range(end_column - 1, start_column - 1, -1)
        ]

        if operator_char == '+':
            value = sum(numbers)
        else:
            value = 1
            for number in numbers:
                value *= number

        grand_total += value

    return grand_total


def main():
    examples = [
        (
            """123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +  """,
            4277556,
            3263827,
        )
    ]
    day = int(__file__.split('/')[-1].split('.')[0][-2:])
    run_puzzle(day, part_a, part_b, examples)


if __name__ == '__main__':
    main()
