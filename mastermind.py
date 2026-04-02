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
print("Answer", m.answer)

combos = set(product("123456", repeat=4))

guess = ["1", "1", "2", "2"]
turn = 0
while True:
    turn += 1
    output = m.check_guess("".join(guess))
    if output[0] == 4:
        break
    print("Turn", turn, "Guess", guess, "Output", output)

    pruned_combos = set()
    guess_count = Counter(guess)
    for combo in combos:
        if output == check_two(guess, combo):
            pruned_combos.add(combo)
    print("Pruned", len(combos) - len(pruned_combos))
    combos = pruned_combos

    worst_response_scores = Counter()
    for combo in product("123456", repeat=4):
        combo_responses = Counter()
        for pruned_combo in pruned_combos:
            response = check_two(combo, pruned_combo)
            combo_responses[response] += 1
        worst_response_scores[combo] = max(combo_responses.values())

    min_response_score = min(worst_response_scores.values())
    possible_guesses = [
        guess
        for guess in worst_response_scores.keys()
        if worst_response_scores[guess] == min_response_score
    ]
    possible_guesses.sort()

    next_guess = None
    for possible_guess in possible_guesses:
        if possible_guess in combos:
            next_guess = possible_guess
            break

    if not next_guess:
        next_guess = possible_guesses[0]

    guess = next_guess

print("Won in turn", turn, "Answer", guess)
