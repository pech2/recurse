# Mastermind in 5 guesses or less

## The Game

Mastermind is a game played by a codemaker and a codebreaker. The codemaker creates a code hidden from the codebreaker made up of an order of 4 colored pegs. The codebreaker makes up to 10 guesses by choosing a code. The guess will result in a number of black pegs if the guess code has a match with the same color in the same position and a number of white pegs if the code has a match with the same color in the wrong position.

example

## An Approach

When we make a guess we may get 4 black pegs and then we win. But what if we get 1 black peg? We know one color is correct and in the correct position but not which one. We can try keeping one color and changing the others but we may get 1 white peg or 2 white pegs, or 1 black peg and 1 white peg or something else. There are 15 combinations of black and white pegs for each guess.  

0
01 02 03 04
10 11 12 13
20 21 22
30 31
40

## The Solution

When we make a guess we want to remove as many possible codes as possible. So how do we determine that? We look at every code and check for every combination of pegs, how many leftover possible codes will be left. Since we don't know the answer, we don't know which combination of pegs we will get for a guess so we compare the worst peg result for each guess. Then we want to choose the guess with the best score. If we continue to do this, we will prune the possible codes to the answer in at most 5 guesses.
