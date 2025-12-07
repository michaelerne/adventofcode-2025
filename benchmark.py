#!/usr/bin/env python3
import argparse
import importlib
import os
import statistics
import time

from aocd import get_data


def iter_days():
    base_dir = os.path.dirname(__file__)
    for filename in sorted(os.listdir(base_dir)):
        if not filename.startswith("day_") or not filename.endswith(".py"):
            continue
        try:
            day = int(filename.split(".")[0][-2:])
        except ValueError:
            continue
        yield day


def benchmark_part(day, part, iterations):
    module = importlib.import_module(f"day_{day:02d}")
    fn_name = f"part_{part}"
    fn = getattr(module, fn_name, None)

    if fn is None:
        return None

    if day == 25 and part != "a":
        return None

    data = get_data(day=day)

    timings_ns = []
    for _ in range(iterations):
        start = time.perf_counter_ns()
        _ = fn(data)
        end = time.perf_counter_ns()
        timings_ns.append(end - start)

    timings_ms = [t / 1e6 for t in timings_ns]

    return {
        "day": day,
        "part": part,
        "min": min(timings_ms),
        "max": max(timings_ms),
        "mean": statistics.mean(timings_ms),
        "stddev": statistics.stdev(timings_ms) if len(timings_ms) > 1 else 0.0,
        "iterations": iterations,
    }


def main():
    parser = argparse.ArgumentParser(description="Benchmark Advent of Code solutions.")
    parser.add_argument(
        "-n",
        "--iterations",
        type=int,
        default=100,
        help="Number of iterations per day/part (default: 100)",
    )
    args = parser.parse_args()

    iterations = args.iterations
    days = list(iter_days())

    results = []

    print(f"Benchmarking {len(days)} days, {iterations} iterations per part...\n")

    for day in days:
        for part in ("a", "b"):
            stats = benchmark_part(day, part, iterations)
            if stats is not None:
                results.append(stats)

    if not results:
        print("No results (no parts found?).")
        return

    fastest_part = min(results, key=lambda r: r["mean"])
    slowest_part = max(results, key=lambda r: r["mean"])

    day_totals = {}
    for r in results:
        day_totals.setdefault(r["day"], 0.0)
        day_totals[r["day"]] += r["mean"]

    fastest_day_num, fastest_day_mean = min(day_totals.items(), key=lambda kv: kv[1])
    slowest_day_num, slowest_day_mean = max(day_totals.items(), key=lambda kv: kv[1])

    header = f"{'Day':>3} {'Part':>4} {'min [ms]':>10} {'max [ms]':>10} {'mean [ms]':>11} {'stddev [ms]':>11} {'Note':>14}"
    print(header)
    print("-" * len(header))

    for r in sorted(results, key=lambda x: (x["day"], x["part"])):
        note_parts = []
        if r is fastest_part:
            note_parts.append("FASTEST PART")
        if r is slowest_part:
            note_parts.append("SLOWEST PART")
        note = ", ".join(note_parts)

        print(
            f"{r['day']:>3} "
            f"{r['part']:>4} "
            f"{r['min']:10.3f} "
            f"{r['max']:10.3f} "
            f"{r['mean']:11.3f} "
            f"{r['stddev']:11.3f} "
            f"{note:>14}"
        )

    print("\nDay summary (sum of mean of parts):")
    for day in sorted(day_totals):
        note = []
        if day == fastest_day_num:
            note.append("FASTEST DAY")
        if day == slowest_day_num:
            note.append("SLOWEST DAY")
        note_str = ", ".join(note)
        print(f"Day {day:02d}: {day_totals[day]:.3f} ms {('(' + note_str + ')') if note_str else ''}")

    total_min_sum = sum(r["min"] for r in results)
    total_max_sum = sum(r["max"] for r in results)
    total_mean_sum = sum(r["mean"] for r in results)

    print("\nOverall:")
    print(
        f"Fastest part: day {fastest_part['day']:02d} part {fastest_part['part']} "
        f"with mean {fastest_part['mean']:.3f} ms"
    )
    print(
        f"Slowest part: day {slowest_part['day']:02d} part {slowest_part['part']} "
        f"with mean {slowest_part['mean']:.3f} ms"
    )
    print(
        f"Fastest day: day {fastest_day_num:02d} with total mean {fastest_day_mean:.3f} ms"
    )
    print(
        f"Slowest day: day {slowest_day_num:02d} with total mean {slowest_day_mean:.3f} ms"
    )

    print("\nPotential totals (summing over all parts):")
    print(f"  Potential fastest sum (sum of mins):   {total_min_sum:.3f} ms")
    print(f"  Potential slowest sum (sum of maxes):  {total_max_sum:.3f} ms")
    print(f"  Average sum (sum of means):            {total_mean_sum:.3f} ms")


if __name__ == "__main__":
    main()
