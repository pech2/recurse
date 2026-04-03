# Mastermind in 5 Turns or Less

## Background

6 colors (numbers 1-6 in my code)
4 colors in an order

6 * 6 * 6 * 6 combinations = 1296

1296 / 2 = 648
648 / 2 = 324
324 / 2 = 162
162 / 2 = 81
81 / 2 = 41

Needs to be faster than logarithmic

1. Make a guess
2. Make another guess

Since we want the minimize guesses we need to consider the worst case.
Which means we need to score the guesses and choose the least worst one.


Counter({5: 694, 4: 533, 3: 62, 2: 6, 1: 1})
