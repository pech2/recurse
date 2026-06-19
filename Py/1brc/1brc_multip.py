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
            f.readline()  # Read forward to the nearest newline
            end = f.tell()

            if end > file_size:
                end = file_size

            chunks.append((filename, start, end))
            start = end

            if start >= file_size:
                break

    return chunks


def process_chunk_standard(args):
    """
    The worker function. Uses standard buffered I/O instead of mmap.
    """
    filename, start, end = args
    stats = {}

    # Calculate exactly how many bytes this worker is responsible for
    target_chunk_size = end - start
    bytes_processed = 0

    with open(filename, "rb") as f:
        # Jump directly to this worker's starting byte
        f.seek(start)

        # Use the highly optimized C-level file iterator
        for line in f:
            # Track our exact progress through the chunk
            bytes_processed += len(line)

            sep_idx = line.find(b";")
            station = line[:sep_idx]
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

            # Once we have processed our assigned bytes, exit the loop
            if bytes_processed >= target_chunk_size:
                break

    return stats


def true_optimized_standard_io(FILE):
    cores = cpu_count()
    chunks = get_file_chunks(FILE, cores)

    with Pool(cores) as p:
        results = p.map(process_chunk_standard, chunks)

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

    output = []
    for station in sorted(final_stats.keys(), key=lambda x: x.decode("utf-8")):
        name = station.decode("utf-8")
        s = final_stats[station]
        mean = s[2] / s[3]
        output.append(f"{name}={s[0]:.1f}/{mean:.1f}/{s[1]:.1f}")

    print("{" + ", ".join(output) + "}")
    return final_stats


import timeit


def profile_timeit(func, iterations=3):
    execution_time = timeit.timeit(stmt=func, number=iterations)
    return round(execution_time / iterations, 2)


if __name__ == "__main__":
    FILE = "measurements-1B.txt"

    naive_time = profile_timeit(lambda: true_optimized_standard_io(FILE))

    print(f"Naive multicore time: {naive_time}s")
