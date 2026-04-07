use std::fs;

fn part1(input: &str) -> i32 {
    let lines = input.split('\n');
    let mut areas = 0;
    for line in lines {
        if line.is_empty() {
            break;
        }
        let mut sides = line.split('x').map(|x| x.parse().unwrap());
        let l: i32 = sides.next().unwrap();
        let w: i32 = sides.next().unwrap();
        let h: i32 = sides.next().unwrap();

        let area = (2 * l * w) + (2 * l * h) + (2 * w * h);
        let smallest_side = std::cmp::min(std::cmp::min(l * w, l * h), w * h);
        areas += area + smallest_side;
    }
    return areas;
}

fn part2(input: &str) -> i32 {
    let lines = input.split('\n');
    let mut lengths = 0;
    for line in lines {
        if line.is_empty() {
            break;
        }
        let mut sides = line.split('x').map(|x| x.parse().unwrap());
        let l: i32 = sides.next().unwrap();
        let w: i32 = sides.next().unwrap();
        let h: i32 = sides.next().unwrap();

        let mut length = l + l + w + w + h + h - std::cmp::max(std::cmp::max(l, w), h) * 2;
        length += l * w * h;
        lengths += length;
    }
    return lengths;
}

fn read_input(file_name: &str) -> String {
    return fs::read_to_string(file_name).expect("Should have been able to read the file");
}

fn main() {
    let e1 = "2x3x4";
    let e2 = "1x1x10";
    println!("e1 {}", part1(e1));
    println!("e2 {}", part1(e2));
    let content = read_input("input");
    println!("p1 {}", part1(&content));

    println!("p2e1 {}", part2(e1));
    println!("p2e2 {}", part2(e2));
    println!("p2 {}", part2(&content));
}
