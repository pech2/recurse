const VOWELS: &'static str = "aeiou";
use std::fs;

fn read_input(file_name: &str) -> String {
    return fs::read_to_string(file_name).expect("Should have been able to read the file");
}

fn part1(input: &str) -> i32 {
    if input.is_empty() {
        return 0;
    }

    let mut vowel_count = 0;
    let mut twice = false;
    let mut prev = '\0';
    let mut magic = false;

    for c in input.chars() {
        if VOWELS.contains(c) {
            vowel_count += 1
        }

        if prev == 'a' && c == 'b' {
            magic = true;
        }
        if prev == 'c' && c == 'd' {
            magic = true;
        }
        if prev == 'p' && c == 'q' {
            magic = true;
        }
        if prev == 'x' && c == 'y' {
            magic = true;
        }

        if prev == c {
            twice = true;
        }
        prev = c;
    }
    if vowel_count < 3 || twice == false {
        return 0;
    }
    if magic == true {
        return 0;
    }

    return 1;
}

fn part2(input: &str) -> i32 {
    if input.is_empty() {
        return 0;
    }
    let chars: Vec<char> = input.chars().collect();
    let mut has_pairs = false;
    for i in 0..chars.len() - 2 {
        for j in i + 2..chars.len() - 1 {
            if chars[i] == chars[j] && chars[i + 1] == chars[j + 1] {
                has_pairs = true;
                break;
            }
        }
        if has_pairs == true {
            break;
        }
    }

    let mut has_letter_between = false;
    for i in 2..chars.len() {
        if chars[i] == chars[i - 2] {
            has_letter_between = true;
            break;
        }
    }

    if has_pairs == true && has_letter_between == true {
        return 1;
    }
    return 0;
}

fn main() {
    let e1 = "ugknbfddgicrmopn";
    println!("e1 t {}", part1(e1));
    let e2 = "aaa";
    println!("e2 t {}", part1(e2));
    let e3 = "jchzalrnumimnmhp";
    println!("e3 f {}", part1(e3));
    let e4 = "haegwjzuvuyypxyu";
    println!("e4 f {}", part1(e4));
    let e5 = "dvszwmarrgswjxmb";
    println!("e5 f {}", part1(e5));

    println!(
        "p1 {}",
        read_input("input").split('\n').map(part1).sum::<i32>()
    );

    let e6 = "qjhvhtzxzqqjkmpb";
    let e7 = "xxyxx";
    let e8 = "uurcxstgmygtbstg";
    let e9 = "ieodomkazucvgmuy";
    println!("e6 t {}", part2(e6));
    println!("e7 t {}", part2(e7));
    println!("e8 f {}", part2(e8));
    println!("e9 f {}", part2(e9));
    println!(
        "p2 {}",
        read_input("input").split('\n').map(part2).sum::<i32>()
    );
}
