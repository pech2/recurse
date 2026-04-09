fn main() {
    let input = std::fs::read_to_string("input").expect("Failed to read input");

    let total_joltage: u32 = input
        .lines()
        .filter(|line| !line.is_empty())
        .map(|bank| find_max_joltage(bank))
        .sum();

    let total_joltage2: u64 = input
        .lines()
        .filter(|line| !line.is_empty())
        .map(|bank| find_max_joltage_part2(bank, 12))
        .sum();
    println!("part1: {}", total_joltage);

    println!("part2: {}", total_joltage2);
}

fn find_max_joltage(bank: &str) -> u32 {
    let mut digits = bank.chars().filter_map(|c| c.to_digit(10));

    let mut max_seen = match digits.next() {
        Some(d) => d,
        None => return 0,
    };

    let mut overall_max = 0;

    for current in digits {
        overall_max = overall_max.max(max_seen * 10 + current);
        max_seen = max_seen.max(current);
    }

    overall_max
}

fn find_max_joltage_part2(bank: &str, k: usize) -> u64 {
    let digits: Vec<u32> = bank.chars().filter_map(|c| c.to_digit(10)).collect();
    let n = digits.len();

    let mut to_discard = n - k;
    let mut stack = Vec::with_capacity(k);

    for digit in digits {
        while to_discard > 0 && !stack.is_empty() && digit > *stack.last().unwrap() {
            stack.pop();
            to_discard -= 1;
        }
        stack.push(digit);
    }

    stack.truncate(k);

    stack.into_iter().fold(0, |acc, d| acc * 10 + d as u64)
}
