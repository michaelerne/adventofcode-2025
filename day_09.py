from itertools import combinations

from run_util import run_puzzle


def parse_data(data):
    return [tuple(map(int, line.strip().split(','))) for line in data.strip().splitlines()]


def part_a(data):
    points = parse_data(data)
    best = 0
    for (x1, y1), (x2, y2) in combinations(points, 2):
        if x1 != x2 and y1 != y2:
            area = (abs(x2 - x1) + 1) * (abs(y2 - y1) + 1)
            if area > best:
                best = area
    return best


def preprocess_segments(points):
    """
    >>> vertical, horizontal = preprocess_segments([(0,0),(4,0),(4,4),(0,4)])
    >>> vertical
    [(4, 0, 4), (0, 0, 4)]
    >>> horizontal
    [(0, 0, 4), (4, 0, 4)]
    """
    vertical_segments = []
    horizontal_segments = []
    point_count = len(points)

    for index in range(point_count):
        (x1, y1) = points[index]
        (x2, y2) = points[(index + 1) % point_count]

        if x1 == x2:
            low_y, high_y = (y1, y2) if y1 < y2 else (y2, y1)
            vertical_segments.append((x1, low_y, high_y))
        else:
            low_x, high_x = (x1, x2) if x1 < x2 else (x2, x1)
            horizontal_segments.append((y1, low_x, high_x))

    return vertical_segments, horizontal_segments


def edge_cuts_rectangle(min_x, max_x, min_y, max_y, vertical_segments, horizontal_segments):
    """
    >>> edge_cuts_rectangle(1,3,1,3, [(2,0,5)], [])
    True
    >>> edge_cuts_rectangle(1,3,1,3, [(0,0,5)], [])
    False
    """
    for segment_x, low_y, high_y in vertical_segments:
        if min_x < segment_x < max_x and max(min_y, low_y) < min(max_y, high_y):
            return True
    for segment_y, low_x, high_x in horizontal_segments:
        if min_y < segment_y < max_y and max(min_x, low_x) < min(max_x, high_x):
            return True
    return False


def center_inside(min_x, max_x, min_y, max_y, vertical_segments):
    """
    >>> segments = [(4,0,4),(0,0,4)]
    >>> center_inside(1,3,1,3,segments)
    True
    >>> center_inside(10,12,10,12,segments)
    False
    """
    center_x_times2 = min_x + max_x
    center_y_times2 = min_y + max_y

    count = 0
    for segment_x, low_y, high_y in vertical_segments:
        if 2 * segment_x > center_x_times2:
            if 2 * low_y < center_y_times2 < 2 * high_y:
                count += 1

    return (count & 1) == 1



def part_b(data):
    points = parse_data(data)
    if not points:
        return 0

    vertical_segments, horizontal_segments = preprocess_segments(points)

    best = 0
    for (x1, y1), (x2, y2) in combinations(points, 2):
        if x1 == x2 or y1 == y2:
            continue

        min_x, max_x = (x1, x2) if x1 < x2 else (x2, x1)
        min_y, max_y = (y1, y2) if y1 < y2 else (y2, y1)

        area = (max_x - min_x + 1) * (max_y - min_y + 1)
        if area <= best:
            continue

        if edge_cuts_rectangle(min_x, max_x, min_y, max_y, vertical_segments, horizontal_segments):
            continue

        if not center_inside(min_x, max_x, min_y, max_y, vertical_segments):
            continue

        best = area

    return best


def main():
    examples = [
        ("""7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3""", 50, 24)
    ]
    day = int(__file__.split('/')[-1].split('.')[0][-2:])
    run_puzzle(day, part_a, part_b, examples)


if __name__ == '__main__':
    main()
