import numpy as np
from scipy.spatial import Delaunay
from scipy.spatial.distance import pdist

from run_util import run_puzzle


def parse_data(data):
    rows = [tuple(map(int, line.split(","))) for line in data.splitlines()]
    return np.asarray(rows, dtype=np.int64)


def dsu_init(n: int):
    parent = list(range(n))
    size = [1] * n
    return parent, size


def dsu_find(parent, x: int) -> int:
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x


def dsu_union(parent, size, a: int, b: int) -> bool:
    ra = dsu_find(parent, a)
    rb = dsu_find(parent, b)
    if ra == rb:
        return False
    if size[ra] < size[rb]:
        ra, rb = rb, ra
    parent[rb] = ra
    size[ra] += size[rb]
    return True


def _condensed_row_starts(n: int) -> np.ndarray:
    i = np.arange(n, dtype=np.int64)
    return n * i - (i * (i + 1)) // 2


def _pairs_from_condensed_indices(n: int, k: np.ndarray, starts: np.ndarray):
    i = np.searchsorted(starts, k, side="right") - 1
    offset = k - starts[i]
    j = i + 1 + offset
    return i.astype(np.int64), j.astype(np.int64)


def part_a(data):
    points = parse_data(data)
    n = int(points.shape[0])

    k_edges = 10 if n == 20 else 1000

    dist2 = pdist(points, metric="sqeuclidean")
    m = dist2.shape[0]

    k_edges = min(k_edges, m)
    k_idx = np.argpartition(dist2, k_edges - 1)[:k_edges]

    starts = _condensed_row_starts(n)
    i, j = _pairs_from_condensed_indices(n, k_idx, starts)

    d = dist2[k_idx]
    order = np.lexsort((j, i, d))
    i = i[order]
    j = j[order]

    parent, size = dsu_init(n)

    for a, b in zip(i, j):
        dsu_union(parent, size, int(a), int(b))

    counts = {}
    for idx in range(n):
        root = dsu_find(parent, idx)
        counts[root] = counts.get(root, 0) + 1

    sizes = sorted(counts.values(), reverse=True)
    while len(sizes) < 3:
        sizes.append(1)

    return sizes[0] * sizes[1] * sizes[2]


def part_b(data):
    points = parse_data(data)
    n = int(points.shape[0])

    tri = Delaunay(points, qhull_options="QJ")
    simplices = tri.simplices

    a = simplices[:, [0, 0, 0, 1, 1, 2]].reshape(-1)
    b = simplices[:, [1, 2, 3, 2, 3, 3]].reshape(-1)
    edges = np.stack([a, b], axis=1).astype(np.int64)

    edges.sort(axis=1)
    edges = np.unique(edges, axis=0)

    i = edges[:, 0]
    j = edges[:, 1]

    dx = points[i, 0] - points[j, 0]
    dy = points[i, 1] - points[j, 1]
    dz = points[i, 2] - points[j, 2]
    dist2 = dx * dx + dy * dy + dz * dz

    order = np.lexsort((j, i, dist2))
    i = i[order]
    j = j[order]

    parent, size = dsu_init(n)
    remaining = n

    for a_idx, b_idx in zip(i, j):
        if dsu_union(parent, size, int(a_idx), int(b_idx)):
            remaining -= 1
            if remaining == 1:
                return int(points[int(a_idx), 0] * points[int(b_idx), 0])

    return None


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


if __name__ == "__main__":
    main()
