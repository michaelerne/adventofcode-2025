from run_util import run_puzzle


def parse_data(data):
    region_block = data[data.rfind("\n\n") + 2:]

    regions = []
    for line in region_block.splitlines():
        dims, counts_list = line.split(": ")
        w, h = map(int, dims.split("x"))
        counts = sum(map(int, counts_list.split()))
        regions.append((w, h, counts))
    return regions


def part_a(data):
    regions = parse_data(data)
    return sum(
        total_presents <= (w // 3) * (h // 3)
        for w, h, total_presents in regions
    )


def main():
    examples = [
        ("", None, None)
    ]
    day = int(__file__.split("/")[-1].split(".")[0][-2:])
    run_puzzle(day, part_a, None, examples)


if __name__ == "__main__":
    main()
