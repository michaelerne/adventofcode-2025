from itertools import combinations

from run_util import run_puzzle


def parse_data(data):
    data = data.strip()
    points = []
    for line in data.splitlines():
        line = line.strip()
        x_str, y_str = line.split(",")
        points.append((int(x_str), int(y_str)))
    return points


def part_a(data):
    points = parse_data(data)
    best_area = 0

    for (x1, y1), (x2, y2) in combinations(points, 2):
        area = (abs(x1 - x2) + 1) * (abs(y1 - y2) + 1)
        if area > best_area:
            best_area = area

    return best_area


def rectangle_area(x_a, y_a, x_b, y_b):
    return (abs(x_a - x_b) + 1) * (abs(y_a - y_b) + 1)


def fits(red_vertices, x_a, y_a, x_b, y_b):
    if not red_vertices:
        return True
    if x_a < x_b:
        x_min, x_max = x_a, x_b
    else:
        x_min, x_max = x_b, x_a
    if y_a < y_b:
        y_min, y_max = y_a, y_b
    else:
        y_min, y_max = y_b, y_a

    for x, y in red_vertices:
        if x_min < x < x_max and y_min < y < y_max:
            return False
    return True


def max_rectangle(half_vertices):
    if len(half_vertices) < 2:
        return 0
    anchor_x, anchor_y = half_vertices[-1]
    other_vertices = half_vertices[:-1]

    return max(
        rectangle_area(anchor_x, anchor_y, b_x, b_y)
        for b_x, b_y in other_vertices
        if fits(other_vertices, anchor_x, anchor_y, b_x, b_y)
    )


def part_b(data):
    points = parse_data(data)
    split_index = len(points) // 2 + 1

    return max(
        max_rectangle(points[:split_index]),
        max_rectangle(points[-2:split_index - 1:-1])
    )


def main():
    example_input = """7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3"""

    examples = [
        (example_input, 50, None),
    ]

    day = int(__file__.split('/')[-1].split('.')[0][-2:])
    run_puzzle(day, part_a, part_b, examples)


if __name__ == '__main__':
    main()
