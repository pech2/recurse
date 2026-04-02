from collections import Counter
from itertools import product
from random import randint
from typing import Iterable


class Mastermind:
    def __init__(self) -> None:
        self.answer = [str(randint(1, 6)) for _ in range(4)]

    def check_guess(self, guess: str):
        black = 0
        white = 0

        for a, g in zip(self.answer, guess):
            if a == g:
                black += 1

        white = sum((Counter(guess) & Counter(self.answer)).values()) - black
        return (black, white)


def check_two(guess: Iterable[str], combo: Iterable[str]):
    black = 0
    white = 0

    for a, g in zip(guess, combo):
        if a == g:
            black += 1

    white = sum((Counter(guess) & Counter(combo)).values()) - black
    return (black, white)


m = Mastermind()

combos = set(product("123456", repeat=4))

guess = ["1", "1", "2", "2"]
turn = 1
output = m.check_guess("".join(guess))
while output[0] != 4:
    print("Turn", turn, "Guess", guess, "Output", output)
    pruned_combos = set()
    guess_count = Counter(guess)
    for combo in combos:
        matches = check_two(guess, combo)
        if matches[0] >= output[0] and matches[1] >= output[1]:
            pruned_combos.add(combo)

    print("Pruned Combos count", len(combos) - len(pruned_combos))
    guess = pruned_combos.pop()
    output = m.check_guess("".join(guess))
    combos = pruned_combos
    turn += 1
print("Won in turn", turn, "Answer", guess)
