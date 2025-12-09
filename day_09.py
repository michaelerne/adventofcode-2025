from run_util import run_puzzle


def parse_data(data):
    return [tuple(map(int, line.strip().split(','))) for line in data.strip().splitlines()]


def part_a(data):
    red_points = parse_data(data)

    best_area = 0
    point_count = len(red_points)

    for index_a in range(point_count):
        ax, ay = red_points[index_a]
        for index_b in range(index_a + 1, point_count):
            bx, by = red_points[index_b]

            min_x = min(ax, bx)
            max_x = max(ax, bx)
            min_y = min(ay, by)
            max_y = max(ay, by)

            width = max_x - min_x + 1
            height = max_y - min_y + 1
            area = width * height

            if area > best_area:
                best_area = area

    return best_area



def part_b(data):
    red_points = parse_data(data)


    def is_point_on_segment(px, py, x1, y1, x2, y2):
        cross = (x2 - x1) * (py - y1) - (y2 - y1) * (px - x1)
        if abs(cross) > 1e-12:
            return False
        if px < min(x1, x2) - 1e-12 or px > max(x1, x2) + 1e-12:
            return False
        if py < min(y1, y2) - 1e-12 or py > max(y1, y2) + 1e-12:
            return False
        return True

    def is_point_in_polygon(px, py, poly):
        inside = False
        n = len(poly)
        for index in range(n):
            x1, y1 = poly[index]
            x2, y2 = poly[(index + 1) % n]

            if is_point_on_segment(px, py, x1, y1, x2, y2):
                return True

            if (y1 > py) != (y2 > py):
                x_intersect = (x2 - x1) * (py - y1) / (y2 - y1) + x1
                if px < x_intersect:
                    inside = not inside

        return inside

    def get_orientation(ax, ay, bx, by, cx, cy):
        v = (bx - ax) * (cy - ay) - (by - ay) * (cx - ax)
        if v > 0:
            return 1
        if v < 0:
            return -1
        return 0

    def do_segments_strictly_intersect(a1, a2, b1, b2):
        (x1, y1) = a1
        (x2, y2) = a2
        (x3, y3) = b1
        (x4, y4) = b2

        o1 = get_orientation(x1, y1, x2, y2, x3, y3)
        o2 = get_orientation(x1, y1, x2, y2, x4, y4)
        o3 = get_orientation(x3, y3, x4, y4, x1, y1)
        o4 = get_orientation(x3, y3, x4, y4, x2, y2)

        return (o1 * o2 < 0) and (o3 * o4 < 0)

    def rectangle_inside_polygon(x1, x2, y1, y2, poly):
        for (cx, cy) in [(x1, y1), (x1, y2), (x2, y1), (x2, y2)]:
            if not is_point_in_polygon(cx, cy, poly):
                return False

        rectangle_edges = [
            ((x1, y1), (x2, y1)),
            ((x2, y1), (x2, y2)),
            ((x2, y2), (x1, y2)),
            ((x1, y2), (x1, y1)),
        ]

        n = len(poly)
        for re_a, re_b in rectangle_edges:
            for index in range(n):
                pe_a = poly[index]
                pe_b = poly[(index + 1) % n]
                if do_segments_strictly_intersect(re_a, re_b, pe_a, pe_b):
                    return False

        return True

    polygon = red_points[:]

    best_area = 0
    point_count = len(red_points)

    for index_a in range(point_count):
        ax, ay = red_points[index_a]
        for index_b in range(index_a + 1, point_count):
            bx, by = red_points[index_b]

            min_x = min(ax, bx)
            max_x = max(ax, bx)
            min_y = min(ay, by)
            max_y = max(ay, by)

            if rectangle_inside_polygon(min_x, max_x, min_y, max_y, polygon):
                width = max_x - min_x + 1
                height = max_y - min_y + 1
                area = width * height
                if area > best_area:
                    best_area = area

    return best_area


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
