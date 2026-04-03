test = [
"L68",
"L30",
"R48",
"L5",
"R60",
"L55",
"L1",
"L99",
"R14",
"L82",
]

def part1():
    start = 50
    zeroes = 0

    turns = read()

    for turn in turns:
        direction = turn[0]
        num = int(turn[1:])
        if direction == "L":
            start -= num
        else:
            start += num

        start %= 100

        if start == 0: zeroes += 1

    return zeroes

def main():
    start = 50
    zeroes = 0

    turns = read()

    for turn in turns:
        direction = turn[0]
        num = int(turn[1:])
        if direction == "L":
            start -= num
        else:
            start += num

        while start < 0:
            start += 100
            zeroes += 1
        while start > 99:
            start -= 100
            zeroes += 1

        if start == 0:
            zeroes += 1

    return zeroes

def part2():
    start = 50
    zeroes = 0
    turns = test
    turns = read()

    for turn in turns:
        num = int(turn[1:])

        if turn[0] == "L":
            num *= -1
            if start == 0:
                start = 100

        start += num
        
        while start < 0:
            start += 100
            zeroes += 1
        while start > 100:
            start -= 100
            zeroes += 1
        if start == 0 or start == 100:
            start = 0 
            zeroes += 1

    return zeroes

def read():
    text = []
    with open(".input") as f:
        for line in f:
            text.append(line.strip())
    return text

if __name__ == "__main__":
    out = part1()
    print(out)

    out = part2()
    print(out) # 6616

    # 6591
    # 6507
    # 6247
    # 6406
