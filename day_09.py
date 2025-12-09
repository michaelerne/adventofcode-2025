from run_util import run_puzzle
from itertools import combinations

def parse_data(data):
    return [tuple(map(int, line.strip().split(','))) for line in data.strip().splitlines()]


def part_a(data):
    points = parse_data(data)
    best = 0

    # return max(
    #     (abs(x2 - x1) + 1) * (abs(y2 - y1) + 1)
    #     for (x1, y1), (x2, y2) in combinations(points, 2)
    #     if x1 != x2 and y1 != y2
    # )

    for (x1, y1), (x2, y2) in combinations(points, 2):
        if x1 != x2 and y1 != y2:
            area = (abs(x2 - x1) + 1) * (abs(y2 - y1) + 1)
            if area > best:
                best = area
    return best


def build_segments(points):
    """
    >>> build_segments([(1,1), (2,1), (2,2)])
    [((1, 1), (2, 1)), ((2, 1), (2, 2)), ((2, 2), (1, 1))]
    """
    return list(zip(points, points[1:] + points[:1]))

def edge_cuts_rectangle(min_x, max_x, min_y, max_y, segments):
    """
    >>> segments = [((2,0),(2,5))]
    >>> edge_cuts_rectangle(1,3,1,3,segments)
    True

    >>> segments = [((0,0),(0,5))]
    >>> edge_cuts_rectangle(1,3,1,3,segments)
    False
    """
    for (x1, y1), (x2, y2) in segments:
        if x1 == x2:  # vertical
            sx = x1
            if not (min_x < sx < max_x):
                continue
            lo, hi = sorted((y1, y2))
            if max(min_y, lo) < min(max_y, hi):
                return True
        else:  # horizontal
            sy = y1
            if not (min_y < sy < max_y):
                continue
            lo, hi = sorted((x1, x2))
            if max(min_x, lo) < min(max_x, hi):
                return True
    return False

def center_inside(min_x, max_x, min_y, max_y, segments):
    """
    >>> segments = [((0,0),(4,0)),((4,0),(4,4)),((4,4),(0,4)),((0,4),(0,0))]
    >>> center_inside(1,3,1,3,segments)
    True

    >>> center_inside(10,12,10,12,segments)
    False
    """
    cx = (min_x + max_x) / 2.0
    cy = (min_y + max_y) / 2.0

    crossings = 0
    for (x1, y1), (x2, y2) in segments:
        if x1 != x2 or x1 <= cx:
            continue
        lo, hi = (y1, y2) if y1 < y2 else (y2, y1)
        if lo < cy < hi:
            crossings += 1
    return crossings % 2 == 1


def part_b(data):
    points = parse_data(data)
    if not points:
        return 0

    segments = build_segments(points)
    best = 0

    for (x1, y1), (x2, y2) in combinations(points, 2):
        if x1 == x2 or y1 == y2:
            continue

        min_x, max_x = min(x1, x2), max(x1, x2)
        min_y, max_y = min(y1, y2), max(y1, y2)

        area = (max_x - min_x + 1) * (max_y - min_y + 1)
        if area <= best:
            continue

        if edge_cuts_rectangle(min_x, max_x, min_y, max_y, segments):
            continue

        if not center_inside(min_x, max_x, min_y, max_y, segments):
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
