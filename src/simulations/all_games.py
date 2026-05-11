"""Script to simulate all possible games and in how many attempts we would win them."""

import json

import matplotlib.pyplot as plt
import numpy as np

from src.config import config
from src.wordle import Wordle


def _plot_results(words_dict: dict[str, int]) -> None:
    """Generates histogram and boxplot of attempts distribution.

    Args:
        words_dict: Dictionary mapping words to number of attempts.
    """

    all_attempts = list(words_dict.values())
    mean = np.mean(all_attempts)
    std = np.std(all_attempts)
    title_suffix = f"(Mean: {mean:.2f}, Std: {std:.2f})"

    # Histogram
    plt.figure()
    plt.hist(
        all_attempts,
        bins=range(1, max(all_attempts) + 2),
        edgecolor="black",
        align="left",
    )
    plt.xlabel("Attempts")
    plt.ylabel("Frequency")
    plt.title(f"Distribution of attempts {title_suffix}")
    plt.savefig(config.paths.histogram, dpi=150, bbox_inches="tight")
    plt.close()

    # Boxplot
    plt.figure()
    plt.boxplot(all_attempts, vert=False)
    plt.xlabel("Attempts")
    plt.title(f"Boxplot of attempts {title_suffix}")
    plt.savefig(config.paths.boxplot, dpi=150, bbox_inches="tight")
    plt.close()

    print(f"Mean: {mean:.2f}. Std: {std:.2f}.")


def main() -> None:
    """Simulates all games and obtains in how many attempts we would win them."""

    # Simulate all games and save results
    words_dict = {}
    for i, word in enumerate(config.possible_words):
        model = Wordle()
        attempts = model.simulate_game(word)
        words_dict[word] = attempts
        if i % 100 == 0:
            print(i)
    with open(config.paths.all_games, "w", encoding="utf-8") as f:
        json.dump(words_dict, f)

    # Plot results
    _plot_results(words_dict)


if __name__ == "__main__":
    main()
