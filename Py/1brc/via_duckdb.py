from time import perf_counter

import duckdb

FILE = "measurements-1B.txt"


# start = perf_counter()
# duckdb.sql(f"""
#   SELECT station, min(temp), avg(temp), max(temp)
#   FROM read_csv('{FILE}', delim=';', header=false,
#                 columns={{'station':'VARCHAR','temp':'DOUBLE'}})
#   GROUP BY station ORDER BY station
# """).show()

# end = perf_counter()
# print(f"Time elapsed: {round(end - start, 2)} seconds")

# After your multiprocessing block, in the same script

t = perf_counter()
import polars as pl

df = (
    pl.scan_csv(FILE, separator=";", has_header=False, new_columns=["station", "temp"])
    .group_by("station")
    .agg(
        [
            pl.col("temp").min().alias("min"),
            pl.col("temp").mean().alias("mean"),
            pl.col("temp").max().alias("max"),
        ]
    )
    .sort("station")
    .collect(engine="streaming")
)
print(f"polars: {perf_counter() - t:.2f}s")

t = perf_counter()

duckdb.sql(f"""SELECT station, min(temp), avg(temp), max(temp)
               FROM read_csv('{FILE}', delim=';', header=false,
                             columns={{'station':'VARCHAR','temp':'DOUBLE'}})
               GROUP BY station ORDER BY station""").fetchall()
print(f"duckdb: {perf_counter() - t:.2f}s")
