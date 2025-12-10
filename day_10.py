import re
from collections import deque
from fractions import Fraction

from run_util import run_puzzle


def parse_data(data):
    data = data.strip()
    if not data:
        return []

    lines = [line.strip() for line in data.splitlines() if line.strip()]

    machines = []
    pattern_re = re.compile(r"\[([.#]+)]")
    buttons_re = re.compile(r"\(([^)]*)\)")
    curly_re = re.compile(r"\{([^}]*)}")

    for line in lines:
        pattern_match = pattern_re.search(line)
        pattern_string = pattern_match.group(1)

        button_strings = buttons_re.findall(line)
        buttons = []
        for button_text in button_strings:
            button_text = button_text.strip()
            indices = tuple(
                int(part.strip())
                for part in button_text.split(",")
                if part.strip() != ""
            )
            buttons.append(indices)

        joltages = []
        curly_match = curly_re.search(line)
        if curly_match:
            joltages_text = curly_match.group(1).strip()
            joltages = [
                int(part.strip())
                for part in joltages_text.split(",")
                if part.strip() != ""
            ]

        machines.append((pattern_string, buttons, joltages))

    return machines


def _min_presses_for_machine(pattern_string, buttons):
    num_lights = len(pattern_string)

    goal_mask = 0
    for index, char in enumerate(pattern_string):
        if char == "#":
            goal_mask |= 1 << index

    if goal_mask == 0:
        return 0

    button_masks = []
    for button in buttons:
        mask = 0
        for light_index in button:
            mask |= 1 << light_index
        button_masks.append(mask)

    max_state = 1 << num_lights
    visited = [-1] * max_state
    queue = deque()

    start_state = 0
    visited[start_state] = 0
    queue.append(start_state)

    while queue:
        state = queue.popleft()
        distance = visited[state]

        for button_mask in button_masks:
            next_state = state ^ button_mask
            if visited[next_state] != -1:
                continue

            next_distance = distance + 1
            visited[next_state] = next_distance

            if next_state == goal_mask:
                return next_distance

            queue.append(next_state)

    return None


def _gauss_jordan_rref(A, t):
    m = len(A)
    n = len(A[0]) if m > 0 else 0

    mat = [
        [Fraction(A[row][col]) for col in range(n)] + [Fraction(t[row])]
        for row in range(m)
    ]

    pivot_cols = [-1] * m
    row = 0

    for col in range(n):
        pivot_row = None
        for r in range(row, m):
            if mat[r][col] != 0:
                pivot_row = r
                break

        if pivot_row is None:
            continue

        mat[row], mat[pivot_row] = mat[pivot_row], mat[row]

        pivot_val = mat[row][col]
        if pivot_val != 1:
            for c in range(col, n + 1):
                mat[row][c] /= pivot_val

        for r in range(m):
            if r == row:
                continue
            factor = mat[r][col]
            if factor == 0:
                continue
            for c in range(col, n + 1):
                mat[r][c] -= factor * mat[row][c]

        pivot_cols[row] = col
        row += 1
        if row == m:
            break

    return mat, pivot_cols


def _min_presses_for_machine_joltage(joltages, buttons):
    num_counters = len(joltages)
    num_buttons = len(buttons)

    A = [[0] * num_buttons for _ in range(num_counters)]
    for j, button in enumerate(buttons):
        for index in set(button):
            if 0 <= index < num_counters:
                A[index][j] = 1

    U = [0] * num_buttons
    for j in range(num_buttons):
        contributing_targets = [joltages[i] for i in range(num_counters) if A[i][j] == 1]
        if contributing_targets:
            U[j] = min(contributing_targets)
        else:
            U[j] = 0

    mat, pivot_cols_per_row = _gauss_jordan_rref(A, joltages)
    m = num_counters
    n = num_buttons

    pivot_row_for_col = {}
    for row, col in enumerate(pivot_cols_per_row):
        if col != -1:
            pivot_row_for_col[col] = row

    pivot_cols = sorted(pivot_row_for_col.keys())
    free_cols = [col for col in range(n) if col not in pivot_cols]

    pivot_expr_const = {}
    pivot_expr_coeffs = {}
    for p in pivot_cols:
        row = pivot_row_for_col[p]
        const_term = mat[row][n]
        coeffs = {}
        for f in free_cols:
            if mat[row][f] != 0:
                coeffs[f] = -mat[row][f]
        pivot_expr_const[p] = const_term
        pivot_expr_coeffs[p] = coeffs

    if not free_cols:
        x = [Fraction(0)] * n
        for p in pivot_cols:
            row = pivot_row_for_col[p]
            x[p] = mat[row][n]
        total = 0
        for j in range(n):
            total += int(x[j])
        return total

    best = None

    free_cols_list = list(free_cols)

    def dfs_free(index, free_assignment, partial_free_sum):
        nonlocal best
        if best is not None and partial_free_sum >= best:
            return

        if index == len(free_cols_list):
            x = [Fraction(0)] * n

            for col, val in free_assignment.items():
                x[col] = Fraction(val)

            for p in pivot_cols:
                const_term = pivot_expr_const[p]
                val = const_term
                coeffs = pivot_expr_coeffs[p]
                for f, coef in coeffs.items():
                    val += coef * x[f]
                x[p] = val

            total = 0
            for j in range(n):
                if x[j] < 0:
                    return
                if x[j].denominator != 1:
                    return
                iv = int(x[j])
                if iv > U[j]:
                    return
                total += iv

            if best is None or total < best:
                best = total
            return

        col = free_cols_list[index]
        max_val = U[col]

        for val in range(0, max_val + 1):
            free_assignment[col] = val
            dfs_free(index + 1, free_assignment, partial_free_sum + val)
        del free_assignment[col]

    dfs_free(0, {}, 0)

    return best


def part_a(data):
    machines = parse_data(data)
    total_presses = 0

    for pattern_string, buttons, _joltages in machines:
        presses = _min_presses_for_machine(pattern_string, buttons)
        total_presses += presses

    return total_presses


def part_b(data):
    machines = parse_data(data)
    total_presses = 0

    for index, (_pattern_string, buttons, joltages) in enumerate(machines):
        presses = _min_presses_for_machine_joltage(joltages, buttons)
        total_presses += presses

    return total_presses


def main():
    examples = [
        (
            """[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}""",
            7,
            33,
        )
    ]
    day = int(__file__.split('/')[-1].split('.')[0][-2:])
    run_puzzle(day, part_a, part_b, examples)


if __name__ == '__main__':
    main()
