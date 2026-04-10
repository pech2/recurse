use std::fs;

fn part1(input: &str) -> i32 {
    let mut count = 0;
    for c in input.chars() {
        match c {
            '(' => count += 1,
            ')' => count -= 1,
            _ => println!("{}", c),
        }
    }
    return count;
}

fn part2(input: &str) -> usize {
    let mut floor = 0;
    for (i, c) in input.chars().enumerate() {
        match c {
            '(' => floor += 1,
            ')' => floor -= 1,
            _ => println!("{}", c),
        }
        if floor == -1 {
            return i + 1;
        }
    }
    panic!("No floor found");
}

fn read_input(file_name: &str) -> String {
    return fs::read_to_string(file_name).expect("Should have been able to read the file");
}

fn main() {
    let example1 = "(())";
    println!("0 {}", part1(example1));
    let example2 = "(()";
    println!("1 {}", part1(example2));
    let content = read_input("input");
    println!("part 1 {}", part1(&content));

    let example3 = ")";
    let example4 = "()())";
    println!("p2 1 {}", part2(example3));
    println!("p2 5 {}", part2(example4));
    println!("part 2 {}", part2(&content));
}
