use md5;

fn solve(secret: &str, length: usize) -> i32 {
    for i in 0.. {
        let hash = md5::compute(format!("{secret}{i}"));
        if format!("{hash:x}").starts_with(&"0".repeat(length)) {
            return i;
        }
    }
    panic!();
}

fn main() {
    let e1 = "abcdef";
    let e2 = "pqrstuv";
    // println!("{}", b"0000035".starts_with(b"00000"));
    // println!("{:x}", md5::compute("abcdef609043"));
    println!("e1 {}", solve(e1, 5));
    println!("e2 {}", solve(e2, 5));
    println!("p1 {}", solve("ckczppom", 5));
    println!("p2 {}", solve("ckczppom", 6));
}
