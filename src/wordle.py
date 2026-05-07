"""
Script to play Wodle using Information Theory.
"""

from typing import cast

import numpy as np

from src.config import Cell, Vector, config


class Wordle:
    """Class to represent a Wordle game and obtain the necessary calculations."""

    def __init__(self) -> None:
        """Constructor of the class."""

        self.possible_words = list(config.possible_words)

    @staticmethod
    def _calculate_vector(guess: str, real_word: str) -> Vector:
        """Calculates the output vector.

        Args:
            guess: Introduced word.
            real_word: Real word.

        Returns:
            Response vector.
        """

        v: list[Cell] = [Cell.GREY for _ in range(config.n_letters)]
        remaining: dict[str, int] = {}

        # First pass: mark greens and count remaining letters
        for i, (g, r) in enumerate(zip(guess, real_word)):
            if g == r:
                v[i] = Cell.GREEN
            else:
                remaining[r] = remaining.get(r, 0) + 1

        # Second pass: mark yellows
        for i, letter in enumerate(guess):
            if v[i] == Cell.GREY and remaining.get(letter, 0) > 0:
                v[i] = Cell.YELLOW
                remaining[letter] -= 1

        return cast(Vector, tuple(v))

    def _get_probability_of_vector(self, guess: str, v: Vector) -> float:
        """Calculates the probability of a specific resulting vector if we introduce the
        word guess.

        Args:
            guess: Word we would write.
            v: Resulting vector we would have introducing that word.

        Returns:
            Probability of obtaining that vector introducing the word 'guess'.
        """

        count = 0

        for word in self.possible_words:
            if self._calculate_vector(guess, word) == v:
                count += 1

        return count / len(self.possible_words)

    def get_entropy_of_word(self, guess: str) -> float:
        """Calculates the entropy of word.

        Args:
            guess: Word we introduce.

        Returns:
            Entropy of the word.
        """

        entropy = 0.0

        for vector in config.all_vectors:
            p = self._get_probability_of_vector(guess, vector)
            if p > 0:  # limit when p -> 0 is 0
                entropy -= p * np.log2(p)

        return entropy

    def _reduce_possible_words(self, guess: str, v: Vector) -> None:
        """Updates the list of possible words when we introduce a guess and obtain a
        vector.

        Args:
            guess: Word we introduced.
            v: Vector we obtained.
        """

        self.possible_words = [
            word
            for word in self.possible_words
            if self._calculate_vector(guess, word) == v
        ]

    def _choose_word(self) -> str:
        """Obtains the word with highest entropy.

        Returns:
            Word with highest entropy.
        """

        max_entropy = -1.0  # it would be valid any number < 0 as entropy is always >= 0
        choosen_word = self.possible_words[0]

        for word in self.possible_words:
            word_entropy = self.get_entropy_of_word(word)
            if word_entropy > max_entropy:
                max_entropy = word_entropy
                choosen_word = word

        return choosen_word

    def simulate_game(self, real_word: str, first_guess: str = "raise") -> int:
        """Plays automatically a game.

        Args:
            real_word: Solution.
            first_guess: First guess we introduce.

        Returns:
            Attempts that takes us to succeed.
        """

        # First turn
        attempts = 1
        if first_guess == real_word:
            return attempts
        vector = self._calculate_vector(first_guess, real_word)
        self._reduce_possible_words(first_guess, vector)

        # Rest of the turns
        while True:
            guess = self._choose_word()
            attempts += 1
            if guess == real_word:
                return attempts
            vector = self._calculate_vector(guess, real_word)
            self._reduce_possible_words(guess, vector)

    @staticmethod
    def _obtain_vector_from_input() -> Vector:
        """Obtains the vector from an input. All numbers in the input must be '0'
        (grey), '1' (yellow), or '2' (green).

        Returns:
            Input vector.

        Raises:
            ValueError: If the input is not correct.
        """

        mapping = {"0": Cell.GREY, "1": Cell.YELLOW, "2": Cell.GREEN}
        v_with_numbers = input("\nVector: ")

        if not all(c in mapping for c in v_with_numbers):
            raise ValueError("The vector can only contain 0, 1 and 2.")

        return cast(Vector, tuple(mapping[c] for c in v_with_numbers))

    def play_game(self, first_guess: str = "raise") -> None:
        """Plays a real game. You have to answer 0 if you have not won and 1 if you have
        won. When asked for a vector write a string of N_LETTERS (5) numbers where a 0
        corresponds to grey, 1 to yellow and 2 to green.

        Args:
            first_guess: First guess we introduce.
        """

        # First turn
        turn = 0
        print(f"\n{first_guess}\n")
        win = int(input("Have you won? "))
        if win == 1:
            print("\nCongratulations!")
            return
        v = self._obtain_vector_from_input()
        self._reduce_possible_words(first_guess, v)

        # Rest of the turns
        while True:
            turn += 1
            guess = self._choose_word()
            print("\n" + guess + "\n")
            win = int(input("Have you won? "))
            if win == 1:
                print("\nCongratulations!")
                return
            v = self._obtain_vector_from_input()
            self._reduce_possible_words(guess, v)


if __name__ == "__main__":
    model = Wordle()
    model.play_game()
