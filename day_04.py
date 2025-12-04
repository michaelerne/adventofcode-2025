from collections import deque
from typing import List
from run_util import run_puzzle


def parse_data(data: str) -> List[List[int]]:
    data = data.strip()
    lines = data.splitlines()
    grid = [list(line.strip()) for line in lines]

    roll_index_by_position: dict[tuple[int, int], int] = {}
    roll_positions: List[tuple[int, int]] = []

    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == '@':
                index = len(roll_positions)
                roll_positions.append((x, y))
                roll_index_by_position[(x, y)] = index

    roll_count = len(roll_positions)
    neighbors: List[List[int]] = [[] for _ in range(roll_count)]

    neighbor_deltas = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),            (0, 1),
        (1, -1),   (1, 0),  (1, 1),
    ]

    for node_index, (x, y) in enumerate(roll_positions):
        for d_x, d_y in neighbor_deltas:
            n_x, n_y = x + d_x, y + d_y
            neighbor_index = roll_index_by_position.get((n_x, n_y))
            if neighbor_index is not None:
                neighbors[node_index].append(neighbor_index)

    return neighbors


def part_a(data):
    neighbors = parse_data(data)
    return sum(1 for adj in neighbors if len(adj) < 4)


def part_b(data):
    neighbors = parse_data(data)
    node_count = len(neighbors)

    degrees = [len(adj) for adj in neighbors]
    queue = deque()
    in_queue = [False] * node_count
    removed = [False] * node_count

    for node_index, degree in enumerate(degrees):
        if degree < 4:
            queue.append(node_index)
            in_queue[node_index] = True

    total_removed = 0

    while queue:
        node = queue.popleft()
        if removed[node]:
            continue

        removed[node] = True
        total_removed += 1

        for neighbor in neighbors[node]:
            if removed[neighbor]:
                continue
            degrees[neighbor] -= 1
            if degrees[neighbor] < 4 and not in_queue[neighbor]:
                in_queue[neighbor] = True
                queue.append(neighbor)

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
