from collections import defaultdict
from time import perf_counter


def main():
    mins = defaultdict(lambda: float("inf"))
    maxs = defaultdict(lambda: float("-inf"))
    avgs = defaultdict(list)

    # Bamako;38.8
    with open("measurements-1M.txt") as f:
        for line in f:
            station, temp = line.strip().split(";")
            temp = float(temp)
            mins[station] = min(mins[station], temp)
            maxs[station] = max(maxs[station], temp)
            avgs[station].append(temp)
    for station in mins:
        print(
            f"{station}: {mins[station]}, {sum(avgs[station]) / len(avgs[station]):,.2f}, {maxs[station]}"
        )


if __name__ == "__main__":
    start = perf_counter()
    main()
    end = perf_counter()

    print(f"Time elapsed: {round(end - start, 2)} seconds")
