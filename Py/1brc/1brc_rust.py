import timeit

# We import the Rust module exactly like a standard Python library
import fast_1brc

FILE = "measurements-1B.txt"


def run_rust_extension(filename):
    # Python calls the Rust function.
    # The GIL is completely bypassed during execution.
    results = fast_1brc.process_1brc_rust(filename)

    # Format and print the final results returned from Rust
    output = []
    for station in sorted(results.keys()):
        min_t, mean_t, max_t = results[station]
        output.append(f"{station}={min_t:.1f}/{mean_t:.1f}/{max_t:.1f}")

    print("{" + ", ".join(output) + "}")


if __name__ == "__main__":
    # Benchmark the Rust extension
    runs = 5
    rust_time = timeit.timeit(lambda: run_rust_extension(FILE), number=runs)
    print(f"\nRust Extension Average: {rust_time / runs:.3f} seconds")
