"""Script to calculate the best initial guess, that is, the word with the highest
initial entropy. This is not necessary, but if the first initial guess is precalculated
(as it will always be the same) we save a lot of time. Note that the first guess can be
precalculated but the second and so on no (in practice), because after the first guess
we can obtain a lot of different output vectors."""

import json

from src.config import config
from src.wordle import Wordle


def main() -> None:
    """Calculates the initial entropy for all words."""

    # Obtain entropy for all words and save it in a dictionary
    model = Wordle()
    words_dict = {}
    for i, word in enumerate(config.possible_words):
        entropy = model.get_entropy_of_word(word)
        words_dict[word] = entropy
        if i % 100 == 0:
            print(i)
    with open(config.paths.initial_guess, "w", encoding="utf-8") as f:
        json.dump(words_dict, f)

    # This is just to see what's the best initial word
    with open(config.paths.initial_guess, "r", encoding="utf-8") as f:
        initial_guess = json.load(f)
    top_word = max(initial_guess, key=initial_guess.get)
    print(f"Best initial guess: {top_word}. Entropy: {initial_guess[top_word]:.2f}.")


if __name__ == "__main__":
    main()
