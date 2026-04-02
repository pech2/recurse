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
    
    guess = pruned_combos.pop()
    worst_response_scores = Counter()
    for combo in product("123456", repeat=4):
        combo = ''.join(combo)
        for black in range(5):
            for white in range(5):
                if black + white > 4:
                    continue
                current_response = 0
                for possible_combo in pruned_combos:
                    response = check_two(combo, possible_combo)
                    if response[0] >= black and response[1] >= white:
                        current_response += 1
                        worst_response_scores[combo] = max(worst_response_scores[combo], current_response)
    min_response_score = min(worst_response_scores.values())
    possible_guesses = [guess for guess in worst_response_scores.keys() if worst_response_scores[guess] == min_response_score]
    for possible_guess in possible_guesses:
        if possible_guess in combos:
            guess = possible_guess
            continue
    guess = possible_guesses.pop()
print("Won in turn", turn, "Answer", guess)
