use memmap2::MmapOptions;
use pyo3::prelude::*;
use rayon::prelude::*;
use std::collections::HashMap;
use std::fs::File;

#[derive(Clone)]
struct Stats {
    min: f64,
    max: f64,
    sum: f64,
    count: u64,
}

#[pyfunction]
fn process_1brc_rust(file_path: String) -> PyResult<HashMap<String, (f64, f64, f64)>> {
    let file = File::open(&file_path)?;
    let mmap = unsafe { MmapOptions::new().map(&file)? };

    let results = mmap
        .par_split(|&b| b == b'\n')
        .filter(|line| !line.is_empty())
        .fold(HashMap::new, |mut acc: HashMap<Vec<u8>, Stats>, line| {
            let sep_idx = line.iter().position(|&b| b == b';').unwrap();

            // Keep it as a borrowed slice, do NOT allocate a Vec yet
            let station_bytes = &line[..sep_idx];

            // Unsafe bypasses UTF-8 validation overhead since we know the 1BRC format is strict
            let temp_str = unsafe { std::str::from_utf8_unchecked(&line[sep_idx + 1..]) };
            let temp: f64 = temp_str.parse().unwrap();

            // Look up using the borrowed slice to avoid 1 billion memory allocations
            if let Some(entry) = acc.get_mut(station_bytes) {
                if temp < entry.min {
                    entry.min = temp;
                }
                if temp > entry.max {
                    entry.max = temp;
                }
                entry.sum += temp;
                entry.count += 1;
            } else {
                // Only allocate memory for the 41k unique stations
                acc.insert(
                    station_bytes.to_vec(),
                    Stats {
                        min: temp,
                        max: temp,
                        sum: temp,
                        count: 1,
                    },
                );
            }
            acc
        })
        .reduce(HashMap::new, |mut a, b| {
            // b is consumed here, so k is moved. No extra allocations happen during the merge!
            for (k, v) in b {
                let entry = a.entry(k).or_insert(Stats {
                    min: v.min,
                    max: v.max,
                    sum: 0.0,
                    count: 0,
                });
                if v.min < entry.min {
                    entry.min = v.min;
                }
                if v.max > entry.max {
                    entry.max = v.max;
                }
                entry.sum += v.sum;
                entry.count += v.count;
            }
            a
        });

    // Format the final output for Python
    let mut final_map = HashMap::new();
    for (station_bytes, stats) in results {
        let name = String::from_utf8(station_bytes).unwrap();
        let mean = stats.sum / (stats.count as f64);
        final_map.insert(name, (stats.min, mean, stats.max));
    }

    Ok(final_map)
}

// Updated to the PyO3 0.21+ Bound API signature
#[pymodule]
fn fast_1brc(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(process_1brc_rust, m)?)?;
    Ok(())
}
