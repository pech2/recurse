test = []


def part1(text):
    count = 0
    nums = text.split(",")
    for range_ in nums:
        left, right = range_.split("-")
        for num in range(int(left), int(right) + 1):
            num_len = len(str(num))
            num_left, num_right = str(num)[: num_len // 2], str(num)[num_len // 2 :]
            if num_left == num_right:
                count += num
    return count


def part2(text):
    count = 0
    nums = text.split(",")
    for range_ in nums:
        left, right = range_.split("-")
        for num in range(int(left), int(right) + 1):
            for i in range(1, len(str(num)) // 2 + 1):
                if len(str(num)) % i != 0:
                    continue
                times = len(str(num)) // i
                if str(num) == str(num)[:i] * times:
                    count += num
                    break
    return count


def read():
    text = []
    with open("input") as f:
        for line in f:
            text.append(line.strip())
    return text[0]


if __name__ == "__main__":
    text = read()
    example = "11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124"

    out = part1(example)
    print("part 1 example", out)
    out = part1(text)
    print("part 1", out)

    out = part2(example)
    print("part 2 example", out)
    out = part2(text)
    print("part 2", out)
