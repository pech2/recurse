from collections import defaultdict


def main():
    mins = {}
    maxs = {}
    avgs = defaultdict(list)

    # Bamako;38.8
    with open("measurements-1M.txt") as f:
        for line in f:
            station, temp, _ = line.split(";")
            temp = int(temp)
            mins[station] = min(mins[station], temp)
            maxs[station] = max(maxs[station], temp)
            avgs[station].append(temp)


if __name__ == "__main__":
    main()
