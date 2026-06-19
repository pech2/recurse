1M

profile_timeit(naive(FILE)): 2.2
profile_timeit(naive_in_place(FILE)): 1.73
profile_timeit(optimized_inline(FILE)): 2.08
profile_timeit(true_optimized_inline(FILE)): 1.52
profile_timeit(true_optimized_inline_binary(FILE)): 1.49
native multicore: .1
DuckDB Average: 0.056 seconds
Polars Average: 0.017 seconds
Rust Extension Average: 0.011 seconds

1B

DuckDB: 5.082 seconds
Rust Extension: 4.267 seconds
Multiprocessing: 18.21 seconds
naive: 6629 seconds


mp | 18.83
mmap | 24.16
duckdb | 5.08
mp pypy | 6.57
mmap pypy | 8.5
polars | 5.25

naive | 6629.63

10M Times

`uv run -m cProfile -o test.prof main.py`

Method | Time
---|---
Unoptimized | 6.85
stripless | 5.79
defaultdictless | 4.34
binary_read, one dict, sum | 2.54
+no_float | 2.38
+in_line_temp | 2.21
split over rfind | 1.82
split over rfind pypy | .67
multiprocessing | .31


1B Times
Method | Time
---|---
mp | 18.83
mmap | 24.16
duckdb | 5.08
mp pypy | 6.57
mmap pypy | 8.5
polars | 5.25

naive | 6629.63
