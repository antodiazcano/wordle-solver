"""Configuration of the project."""

from dataclasses import dataclass
from enum import IntEnum
from itertools import product
from pathlib import Path
from typing import TypeAlias, cast, get_args


class Cell(IntEnum):
    """Class to define the possible values of a cell."""

    GREY = 0
    YELLOW = 1
    GREEN = 2


Vector: TypeAlias = tuple[Cell, Cell, Cell, Cell, Cell]
n_letters = len(get_args(Vector))


@dataclass
class PathsConfig:
    """Paths configuration class."""

    possible_words: Path = Path("data/possible_words.txt")
    initial_guess: Path = Path("data/initial_guess.json")
    all_games: Path = Path("data/all_games.json")
    histogram: Path = Path("data/histogram.png")
    boxplot: Path = Path("data/boxplot.png")


@dataclass
class Config:
    """
    Main configuration class.
    """

    paths = PathsConfig()
    n_letters = n_letters
    all_vectors: list[Vector] = [
        cast(Vector, combination)
        for combination in product(
            [Cell.GREY, Cell.YELLOW, Cell.GREEN], repeat=n_letters
        )
    ]
    with open(paths.possible_words, "r", encoding="utf-8") as f:
        possible_words = [line.strip() for line in f]


config = Config()
