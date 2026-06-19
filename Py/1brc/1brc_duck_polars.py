import timeit

import duckdb
import polars as pl

FILE = "measurements-1B.txt"


def run_duckdb(filename):
    # DuckDB is written in C++. We write SQL, it compiles it to vectorized SIMD operations.
    query = f"""
        SELECT
            station,
            MIN(temp) AS min_temp,
            AVG(temp) AS mean_temp,
            MAX(temp) AS max_temp
        FROM read_csv(
            '{filename}',
            delim=';',
            header=false,
            columns={{'station': 'VARCHAR', 'temp': 'DOUBLE'}}
        )
        GROUP BY station
        ORDER BY station
    """
    # .fetchall() forces the engine to actually execute the query
    return duckdb.sql(query).fetchall()


def run_polars(filename):
    # Polars is written in Rust. We MUST use scan_csv (Lazy API) instead of read_csv (Eager API)
    # so it streams the file rather than trying to load 12GB into RAM all at once.
    df = (
        pl.scan_csv(
            filename,
            separator=";",
            has_header=False,
            new_columns=["station", "temp"],
            schema={"station": pl.String, "temp": pl.Float64},
        )
        .group_by("station")
        .agg(
            pl.col("temp").min().alias("min_temp"),
            pl.col("temp").mean().alias("mean_temp"),
            pl.col("temp").max().alias("max_temp"),
        )
        .sort("station")
        .collect()  # .collect() triggers the Rust execution engine
    )
    return df


if __name__ == "__main__":
    # Run 5 times and calculate the per-call average
    runs = 3

    # print("Benchmarking DuckDB...")
    # duck_total = timeit.timeit(lambda: run_duckdb(FILE), number=runs)
    # print(f"DuckDB Average: {duck_total / runs:.3f} seconds\n")

    print("Benchmarking Polars...")
    polars_total = timeit.timeit(lambda: run_polars(FILE), number=runs)
    print(f"Polars Average: {polars_total / runs:.3f} seconds")
