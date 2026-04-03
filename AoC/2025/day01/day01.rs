use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;

fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
where
    P: AsRef<Path>,
{
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}

fn main() {
    let mut start = 50;
    let mut zeroes = 0;

    if let Ok(lines) = read_lines("./.input") {
        for line in lines.map_while(Result::ok) {
            let (direction, num_str) = line.split_at(1);
            let num: i32 = num_str.parse().expect("Int expected");
            if direction == "L" {
                start -= num;
            } else {
                start += num;
            }
            start %= 100;
            if start == 0 {
                zeroes += 1;
            }
        }
    }
    println!("{}", zeroes);

    start = 50;
    zeroes = 0;

    if let Ok(lines) = read_lines("./.input") {
        for line in lines.map_while(Result::ok) {
            let (direction, num_str) = line.split_at(1);
            let mut num: i32 = num_str.parse().expect("Int expected");
            if direction == "L" {
                num *= -1;
                if start == 0 {
                    start = 100;
                }
            }

            start += num;

            while start < 0 {
                start += 100;
                zeroes += 1;
            }
            while start > 100 {
                start -= 100;
                zeroes += 1;
            }
            if start == 0 || start == 100 {
                start = 0;
                zeroes += 1;
            }
        }
    }
    println!("{}", zeroes);
}
