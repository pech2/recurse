# We don't import anything. The @profile decorator is injected by kernprof.


@profile
def parse_c_optimized(line):
    # Using C-backend .partition and float()
    station, _, temp_str = line.partition(";")
    temp = float(temp_str)
    return station, temp


@profile
def parse_python_vm(line):
    # Using pure Python slicing and concatenation
    sep_idx = line.find(";")
    station = line[:sep_idx]
    temp_str = line[sep_idx + 1 : -1]
    temp = int(temp_str[:-2] + temp_str[-1:])
    return station, temp


@profile
def parse_split(line):
    # Using C-backend .split() and float()
    station, temp_str = line.split(";")
    temp = float(temp_str)
    return station, temp


if __name__ == "__main__":
    test_line = "Zürich;-24.7\n"
    # Run each 1 million times
    for _ in range(1_000):
        parse_c_optimized(test_line)
        parse_python_vm(test_line)
        parse_split(test_line)
