import re
from math import inf

import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds

from run_util import run_puzzle


def parse_data(data):
    data = data.strip()
    if not data:
        return []

    pattern_re = re.compile(r"\[([.#]+)]")
    buttons_re = re.compile(r"\(([^)]*)\)")
    jolts_re = re.compile(r"\{([^}]*)}")

    return [
        (
            pattern_re.search(line).group(1),
            [
                tuple(int(x) for x in btn.split(","))
                for btn in buttons_re.findall(line)
            ],
            [int(x) for x in jolts_re.search(line).group(1).split(",")]
        )
        for line in data.splitlines()
    ]


def part_a(data):
    machines = parse_data(data)
    return sum(
        min_light_presses(pattern_string, buttons)
        for pattern_string, buttons, _joltage_values in machines
    )


from collections import deque


def min_light_presses(pattern_string, buttons):
    num_lights = len(pattern_string)

    goal_mask = sum(
        1 << i
        for i, ch in enumerate(pattern_string)
        if ch == "#"
    )
    button_masks = [
        sum(1 << idx for idx in button)
        for button in buttons
    ]

    visited = [-1] * (1 << num_lights)
    queue = deque([0])
    visited[0] = 0

    while queue:
        state = queue.popleft()
        distance = visited[state]

        for mask in button_masks:
            next_state = state ^ mask
            if visited[next_state] != -1:
                continue

            visited[next_state] = distance + 1
            if next_state == goal_mask:
                return distance + 1
            queue.append(next_state)
    return None


def part_b(data):
    machines = parse_data(data)
    return sum(
        min_presses_joltage(joltage_values, buttons)
        for _pattern_string, buttons, joltage_values in machines
    )


def min_presses_joltage(joltage_values, buttons):
    m = len(joltage_values)
    n = len(buttons)


    c = np.ones(n, dtype=float)
    integrality = np.ones(n, dtype=int)
    bounds = Bounds(
        lb=np.zeros(n, dtype=float),
        ub=np.full(n, inf, dtype=float),
    )

    A_eq = np.array(
        [[1.0 if i in button else 0.0 for button in buttons]
         for i in range(m)],
        dtype=float,
    )
    b_eq = np.array(joltage_values, dtype=float)
    constraint = LinearConstraint(A_eq, lb=b_eq, ub=b_eq)

    result = milp(
        c=c,
        integrality=integrality,
        bounds=bounds,
        constraints=[constraint],
    )

    return int(sum(round(x) for x in result.x))


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
