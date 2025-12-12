# Advent of Code 2025

This repository contains my solutions for **Advent of Code 2025**, covering **all 12 days** using a shared execution boilerplate.

## Philosophy

This year’s focus was **speed**, not aesthetics.

- I deliberately did **not** aim for clean, idiomatic, or reusable code for all days.
- The primary goal was to solve problems **as fast as possible**, both in terms of:
  - **runtime performance**
  - **iteration speed while solving**
- Solutions are often **domain-specific**, aggressively simplified once input structure was understood, and sometimes rely on **input invariants** rather than fully general algorithms.
- Solutions are probably **not** optimal, but what I achieved before heading to work with rare optimizations later on.

If you’re looking for “pretty” AoC solutions, this repo is probably not what you want.  
If you’re interested in **how far you can push CPython with the right insights**, this is.

## Runtime & Environment

- **Interpreter:** CPython
- **Target:** Minimize wall-clock runtime across all inputs
- **Approach:**
  - Prefer simple arithmetic over general algorithms when possible
  - Avoid unnecessary abstractions
  - Trade generality for speed once input properties are clear
  - Use brute force only when it is provably rare or tightly bounded

## Boilerplate

All days share a common runner (`run_util.py`) which handles:

- Input loading
- Example verification
- Timing and output formatting

Each day follows the same basic structure, making it easy to benchmark and compare solutions consistently.

## Examples & Safety

- Some days intentionally **disable example checks** once the real input behavior is fully understood.
- In a few cases, the final solution relies on properties that are true for the **actual puzzle input**, even if the provided example would require a more general solution.
- This is intentional and documented where it happens.

## Benchmark Results

Benchmark results for this year, as produced by benchmark.py:
```
Benchmarking 12 days, 100 iterations per part...

Day Part   min [ms]   max [ms]   mean [ms] stddev [ms]           Note
---------------------------------------------------------------------
  1    a      0.519      3.157       0.720       0.508               
  1    b      0.633      3.204       0.808       0.480               
  2    a     19.411     37.179      21.106       2.285               
  2    b     19.816     36.977      21.376       2.509               
  3    a      0.463      0.574       0.493       0.015               
  3    b      1.068      1.329       1.110       0.030               
  4    a      8.944     17.290      10.003       1.442               
  4    b     10.985     18.983      12.125       1.397               
  5    a      0.267      0.372       0.296       0.021               
  5    b      0.147      0.213       0.162       0.016   FASTEST PART
  6    a      0.912      1.915       0.998       0.116               
  6    b      1.341      1.580       1.426       0.044               
  7    a      0.397      0.498       0.420       0.016               
  7    b      0.549      1.188       0.724       0.247               
  8    a     86.150    110.917      90.084       3.892               
  8    b    302.331    345.437     325.298       9.311   SLOWEST PART
  9    a      9.552     12.020       9.895       0.373               
  9    b      0.770      1.014       0.851       0.059               
 10    a      1.693      2.164       1.831       0.100               
 10    b     88.308    107.886      92.650       4.026               
 11    a      0.127      6.265       0.243       0.660               
 11    b      0.484      2.889       0.617       0.381               
 12    a      0.554      0.799       0.603       0.040               

Day summary (sum of mean of parts):
Day 01: 1.528 ms 
Day 02: 42.482 ms 
Day 03: 1.603 ms 
Day 04: 22.128 ms 
Day 05: 0.458 ms (FASTEST DAY)
Day 06: 2.424 ms 
Day 07: 1.145 ms 
Day 08: 415.381 ms (SLOWEST DAY)
Day 09: 10.746 ms 
Day 10: 94.481 ms 
Day 11: 0.860 ms 
Day 12: 0.603 ms 

Overall:
Fastest part: day 05 part b with mean 0.162 ms
Slowest part: day 08 part b with mean 325.298 ms
Fastest day: day 05 with total mean 0.458 ms
Slowest day: day 08 with total mean 415.381 ms

Potential totals (summing over all parts):
  Potential fastest sum (sum of mins):   555.421 ms
  Potential slowest sum (sum of maxes):  713.850 ms
  Average sum (sum of means):            593.840 ms
```

## Highlights

- Several problems that appear complex or even NP-hard at first glance collapse to **simple arithmetic checks** once the input structure is examined.
- Day 12 is a good example: what initially looks like a 2D packing problem reduces to a constant-time inequality.
- Many solutions are effectively **proofs encoded as code**, rather than general-purpose solvers.

## Disclaimer

These solutions are:

- ✔ correct for the official inputs I tested
- ✔ fast  
- ✘ not defensive  
- ✘ not generalized  
- ✘ not optimized for readability  

And that's by design.
