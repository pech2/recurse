import mmap
import os
from multiprocessing import Pool, cpu_count


def get_file_chunks(filename, num_chunks):
    """
    Divides the file into byte ranges for each CPU core.
    Ensures we don't accidentally split a station name in half.
    """
    file_size = os.path.getsize(filename)
    chunk_size = file_size // num_chunks
    chunks = []

    with open(filename, "rb") as f:
        start = 0
        for _ in range(num_chunks):
            f.seek(start + chunk_size)
            # Read forward to the nearest newline to complete the row
            f.readline()
            end = f.tell()

            # Cap at the actual file size
            if end > file_size:
                end = file_size

            chunks.append((filename, start, end))
            start = end

            if start >= file_size:
                break

    return chunks


def process_chunk(args):
    """
    The worker function. Maps its assigned portion of the file
    directly into RAM and uses fast C-level byte parsing.
    """
    filename, start, end = args
    stats = {}

    # Read as raw bytes to bypass UTF-8 decoding overhead
    with open(filename, "rb") as f:
        # mmap bypasses the OS kernel buffer copy
        with mmap.mmap(f.fileno(), length=0, access=mmap.ACCESS_READ) as mm:
            mm.seek(start)

            while mm.tell() < end:
                line = mm.readline()
                if not line:
                    break

                # C-level byte searching is significantly faster than string splitting
                sep_idx = line.find(b";")
                station = line[:sep_idx]

                # float() natively accepts byte-strings (b'12.3'), no decoding needed
                temp = float(line[sep_idx + 1 : -1])

                if station in stats:
                    s = stats[station]
                    if temp < s[0]:
                        s[0] = temp
                    if temp > s[1]:
                        s[1] = temp
                    s[2] += temp
                    s[3] += 1
                else:
                    stats[station] = [temp, temp, temp, 1]

    return stats


def true_optimized_multicore(FILE):
    # Utilize every available hardware thread
    cores = cpu_count()
    chunks = get_file_chunks(FILE, cores)

    # 1. MAP: Distribute the byte offsets to the worker processes
    with Pool(cores) as p:
        results = p.map(process_chunk, chunks)

    # 2. REDUCE: Merge the partial dictionaries back together
    final_stats = {}
    for partial_stats in results:
        for station, s in partial_stats.items():
            if station in final_stats:
                fs = final_stats[station]
                if s[0] < fs[0]:
                    fs[0] = s[0]
                if s[1] > fs[1]:
                    fs[1] = s[1]
                fs[2] += s[2]
                fs[3] += s[3]
            else:
                final_stats[station] = s

    # 3. FORMAT: Decode the byte-keys and match the 1BRC output spec
    output = []

    # We decode the key for alphabetical sorting to match standard string logic
    for station in sorted(final_stats.keys(), key=lambda x: x.decode("utf-8")):
        name = station.decode("utf-8")
        s = final_stats[station]
        mean = s[2] / s[3]
        output.append(f"{name}={s[0]:.1f}/{mean:.1f}/{s[1]:.1f}")

    print("{" + ", ".join(output) + "}")

    return final_stats


import timeit


def profile_timeit(func, iterations=5):
    execution_time = timeit.timeit(stmt=func, number=iterations)
    return round(execution_time / iterations, 2)


if __name__ == "__main__":
    FILE = "measurements-1M.txt"

    naive_time = profile_timeit(lambda: true_optimized_multicore(FILE))

    print(f"Naive multicore time: {naive_time}s")
