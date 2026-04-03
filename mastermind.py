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


def minimax_guess(m: Mastermind) -> int:
    """Guess the answer in Mastermind using Knuth's Minimax algorithm

    1. Start with guess 1122 which has the best outcome and get a certain response (a combination of black and white pegs).
    2. For each guess we keep track of remaining possible guesses and prune what's possible after each guess.
        a. Prune by keeping only possible guesses that match each guess response.
    3. Calculate next guess by choosing the least worst option.
        a. Score guesses by the least guesses that would be removed from making that guess by simulating all responses for all guesses.
        b. Choose the best of the guesses.
    """
    print("Answer", m.answer)

    # Create a set with all possible guesses
    combos = set(product("123456", repeat=4))

    # Start with 1122 because it has an AABB pattern which has the best outcome rather than ABCD
    guess = ["1", "1", "2", "2"]
    turn = 0
    while True:
        turn += 1
        output = m.check_guess("".join(guess))
        if output[0] == 4:
            break
        print("Turn", turn, "Guess", guess, "Output", output)

        # Which check every remaining possible guess to exactly match the response against the guess we made.
        # Match exactly because anything else will not result in an possible answer.
        pruned_combos = set()
        for combo in combos:
            if output == check_two(guess, combo):
                pruned_combos.add(combo)
        print(
            "Pruned", len(combos) - len(pruned_combos), "Remaining", len(pruned_combos)
        )
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
    return turn


def try_all():
    counts = Counter()
    for combo in product("123456", repeat=4):
        m = Mastermind()
        m.answer = combo
        counts[minimax_guess(m)] += 1

    print(counts)


if __name__ == "__main__":
    m = Mastermind()
    minimax_guess(m)
