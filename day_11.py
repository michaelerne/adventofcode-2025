from functools import cache

from run_util import run_puzzle


def count_paths(graph, start_device, target_device, required_devices):
    index_by_device = {name: idx for idx, name in enumerate(required_devices)}
    full_mask = (1 << len(required_devices)) - 1

    @cache
    def dfs(device_name, visited_mask):
        if device_name in index_by_device:
            visited_mask |= 1 << index_by_device[device_name]

        if device_name == target_device:
            return 1 if visited_mask == full_mask else 0

        total_paths = 0
        for next_device in graph.get(device_name, []):
            total_paths += dfs(next_device, visited_mask)
        return total_paths

    return dfs(start_device, 0)


def parse_data(data):
    return {
        source: outputs.split()
        for source, outputs in (
            line.split(":", 1)
            for line in data.splitlines()
        )
    }


def part_a(data):
    graph = parse_data(data)
    return count_paths(graph, "you", "out", ())


def part_b(data):
    graph = parse_data(data)
    return count_paths(graph, "svr", "out", required_devices=("dac", "fft"))


def main():
    examples = [
        (
            """aaa: you hhh
you: bbb ccc
bbb: ddd eee
ccc: ddd eee fff
ddd: ggg
eee: out
fff: out
ggg: out
hhh: ccc fff iii
iii: out""",
            5,
            None,
        ),
        (
            """svr: aaa bbb
aaa: fft
fft: ccc
bbb: tty
tty: ccc
ccc: ddd eee
ddd: hub
hub: fff
eee: dac
dac: fff
fff: ggg hhh
ggg: out
hhh: out""",
            None,
            2,
        ),
    ]
    day = int(__file__.split('/')[-1].split('.')[0][-2:])
    run_puzzle(day, part_a, part_b, examples)


if __name__ == '__main__':
    main()
