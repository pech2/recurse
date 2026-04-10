use std::collections::HashSet;
use std::fs;

fn read_input(file_name: &str) -> String {
    return fs::read_to_string(file_name).expect("Should have been able to read the file");
}

fn part1(input: &str) -> usize {
    let mut coords: HashSet<(i32, i32)> = HashSet::new();
    let mut x = 0;
    let mut y = 0;

    coords.insert((0, 0));
    for c in input.chars() {
        match c {
            '>' => x += 1,
            '<' => x -= 1,
            '^' => y += 1,
            'v' => y -= 1,
            _ => println!("{}", c),
        }
        coords.insert((x, y));
    }
    return coords.len();
}

fn part2(input: &str) -> usize {
    let mut coords: HashSet<(i32, i32)> = HashSet::new();
    let mut santa_x = 0;
    let mut santa_y = 0;
    let mut robo_x = 0;
    let mut robo_y = 0;
    coords.insert((0, 0));

    let mut coord_iter = input.chars();
    loop {
        if let Some(c) = coord_iter.next() {
            match c {
                '>' => santa_x += 1,
                '<' => santa_x -= 1,
                '^' => santa_y += 1,
                'v' => santa_y -= 1,
                _ => println!("{}", c),
            }
            coords.insert((santa_x, santa_y));
        } else {
            break;
        }
        if let Some(c) = coord_iter.next() {
            match c {
                '>' => robo_x += 1,
                '<' => robo_x -= 1,
                '^' => robo_y += 1,
                'v' => robo_y -= 1,
                _ => println!("{}", c),
            }
            coords.insert((robo_x, robo_y));
        } else {
            break;
        }
    }
    return coords.len();
}

fn main() {
    let e1 = ">";
    let e2 = "^>v<";
    let e3 = "^v^v^v^v^v";
    println!("e1 {}", part1(e1));
    println!("e2 {}", part1(e2));
    println!("e3 {}", part1(e3));
    println!("p1 {}", part1(&read_input("input")));

    println!("e1 {}", part2(e1));
    println!("e2 {}", part2(e2));
    println!("e3 {}", part2(e3));
    println!("p2 {}", part2(&read_input("input")));
}
