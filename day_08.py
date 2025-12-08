from run_util import run_puzzle
import heapq
from collections import defaultdict


def parse_data(data):
    data = data.strip()
    return [tuple(map(int, line.split(','))) for line in data.splitlines()]


class DisjointSet:
    def __init__(self, size):
        self.parent = list(range(size))
        self.component_size = [1] * size

    def find(self, index):
        parent = self.parent

        while parent[index] != index:
            parent[index] = parent[parent[index]]
            index = parent[index]
        return index

    def union(self, index_a, index_b):
        root_a = self.find(index_a)
        root_b = self.find(index_b)
        if root_a == root_b:
            return False

        size = self.component_size
        parent = self.parent

        if size[root_a] < size[root_b]:
            root_a, root_b = root_b, root_a
        parent[root_b] = root_a
        size[root_a] += size[root_b]
        return True


def iter_point_pairs(points):
    number_of_points = len(points)
    for index_a in range(number_of_points - 1):
        x1, y1, z1 = points[index_a]
        for index_b in range(index_a + 1, number_of_points):
            x2, y2, z2 = points[index_b]
            dx = x1 - x2
            dy = y1 - y2
            dz = z1 - z2
            distance_squared = dx * dx + dy * dy + dz * dz
            yield distance_squared, index_a, index_b


def part_a(data):
    points = parse_data(data)
    number_of_points = len(points)

    # example data
    if number_of_points == 20:
        max_pairs_to_keep = 10
    else:
        max_pairs_to_keep = 1000

    heap = []

    for distance_squared, index_a, index_b in iter_point_pairs(points):
        if len(heap) < max_pairs_to_keep:
            heapq.heappush(heap, (-distance_squared, index_a, index_b))
        else:
            if -heap[0][0] > distance_squared:
                heapq.heapreplace(heap, (-distance_squared, index_a, index_b))

    edges = []
    while heap:
        negative_distance, index_a, index_b = heapq.heappop(heap)
        edges.append((-negative_distance, index_a, index_b))
    edges.sort(key=lambda entry: entry[0])

    dsu = DisjointSet(number_of_points)

    for distance_squared, index_a, index_b in edges:
        dsu.union(index_a, index_b)

    sizes_by_root = defaultdict(int)
    for index in range(number_of_points):
        root = dsu.find(index)
        sizes_by_root[root] += 1

    all_sizes = sorted(sizes_by_root.values(), reverse=True)

    return all_sizes[0] * all_sizes[1] * all_sizes[2]


def part_b(data):
    points = parse_data(data)
    number_of_points = len(points)

    edges = list(iter_point_pairs(points))
    edges.sort(key=lambda entry: entry[0])

    dsu = DisjointSet(number_of_points)

    components_remaining = number_of_points
    last_merge_edge = None

    for distance_squared, index_a, index_b in edges:
        merged = dsu.union(index_a, index_b)
        if merged:
            components_remaining -= 1
            last_merge_edge = (index_a, index_b)
            if components_remaining == 1:
                break

    index_a, index_b = last_merge_edge
    x_a = points[index_a][0]
    x_b = points[index_b][0]
    return x_a * x_b


def main():
    examples = [
        (
            """162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689""",
            40,
            25272,
        )
    ]
    day = int(__file__.split('/')[-1].split('.')[0][-2:])
    run_puzzle(day, part_a, part_b, examples)


if __name__ == '__main__':
    main()
