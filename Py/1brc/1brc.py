import timeit

FILE = "measurements-1M.txt"


def naive(FILE):
    stats = {}

    with open(FILE) as f:
        for line in f:
            station, temp = line.strip().split(";")
            temp = float(temp)
            if station in stats:
                stats[station] = (
                    min(stats[station][0], temp),
                    max(stats[station][1], temp),
                    stats[station][2] + temp,
                    stats[station][3] + 1,
                )
            else:
                stats[station] = (temp, temp, temp, 1)

    for station in sorted(stats):
        s = stats[station]
        print(f"{station}={s[0]:.1f}/{s[2] / s[3]:.1f}/{s[1]:.1f}")
    return stats


def naive_in_place(FILE):
    stats = {}

    with open(FILE) as f:
        for line in f:
            station, temp = line.strip().split(";")
            temp = float(temp)

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

    for station in sorted(stats):
        s = stats[station]
        print(f"{station}={s[0]:.1f}/{s[2] / s[3]:.1f}/{s[1]:.1f}")

    return stats


def optimized_inline(FILE):
    stats = {}

    with open(FILE, "rb") as f:
        for line in f:
            sep_idx = line.find(b";")
            station = line[:sep_idx]
            temp_str = line[sep_idx + 1 : -1]

            temp = int(temp_str[:-2] + temp_str[-1:])

            try:
                s = stats[station]
                if temp < s[0]:
                    s[0] = temp
                if temp > s[1]:
                    s[1] = temp
                s[2] += temp
                s[3] += 1
            except KeyError:
                stats[station] = [temp, temp, temp, 1]

    results = []
    for station in sorted(stats, key=lambda x: x.decode("utf-8")):
        s = stats[station]
        name = station.decode("utf-8")

        min_val = s[0] / 10
        max_val = s[1] / 10
        mean_val = (s[2] / 10) / s[3]

        results.append(f"{name}={min_val:.1f}/{mean_val:.1f}/{max_val:.1f}")

    print("{" + ", ".join(results) + "}")
    return stats


def true_optimized_inline(FILE):
    stats = {}

    with open(FILE, "r", encoding="utf-8") as f:
        for line in f:
            station, _, temp_str = line.partition(";")
            temp = float(temp_str)

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

    results = []

    for station in sorted(stats):
        s = stats[station]
        mean = s[2] / s[3]

        results.append(f"{station}={s[0]:.1f}/{mean:.1f}/{s[1]:.1f}")

    print("\n".join(results))

    return stats


def true_optimized_inline_binary(FILE):
    stats = {}

    # 1. Open in binary read mode ('rb')
    with open(FILE, "rb") as f:
        # f yields raw byte-strings (e.g., b'Station;12.3\n')
        for line in f:
            # 2. Use a byte-string literal (b";") for the partition
            station, _, temp_str = line.partition(b";")

            # 3. The Magic Trick: float() natively accepts byte-strings!
            # You do NOT need to decode temp_str to parse the number.
            temp = float(temp_str)

            # Dictionary keys are now bytes (e.g., b'Z\xc3\xbcrich')
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

    results = []

    # 4. Decode the keys ONLY at the very end for sorting and printing.
    # We sort by the decoded string to ensure Unicode characters sort correctly.
    for station_bytes in sorted(stats.keys(), key=lambda x: x.decode("utf-8")):
        s = stats[station_bytes]
        mean = s[2] / s[3]

        # Decode the station name exactly once per unique station (~41k times)
        # instead of decoding 1 billion times in the main loop.
        name = station_bytes.decode("utf-8")

        results.append(f"{name}={s[0]:.1f}/{mean:.1f}/{s[1]:.1f}")

    print("\n".join(results))

    return stats


def profile_timeit(func, iterations=5):
    execution_time = timeit.timeit(stmt=func, number=iterations)
    return round(execution_time / iterations, 2)


def main():
    naive_time = profile_timeit(lambda: naive(FILE))
    naive_in_place_time = profile_timeit(lambda: naive_in_place(FILE))
    optimized_inline_time = profile_timeit(lambda: optimized_inline(FILE))
    true_optimized_inline_time = profile_timeit(lambda: true_optimized_inline(FILE))
    true_optimized_inline_binary_time = profile_timeit(
        lambda: true_optimized_inline_binary(FILE)
    )

    print(f"profile_timeit(naive(FILE)): {naive_time}")
    print(f"profile_timeit(naive_in_place(FILE)): {naive_in_place_time}")
    print(f"profile_timeit(optimized_inline(FILE)): {optimized_inline_time}")
    print(f"profile_timeit(true_optimized_inline(FILE)): {true_optimized_inline_time}")
    print(
        f"profile_timeit(true_optimized_inline_binary(FILE)): {true_optimized_inline_binary_time}"
    )


if __name__ == "__main__":
    main()
