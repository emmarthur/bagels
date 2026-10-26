"""
Bagels clue logic shared by the reference script and the web app.

A secret is NUM_DIGITS unique digits. For each guess digit:
Fermi means right digit in the right place, Pico means right digit in the
wrong place, and Bagels means nothing matched. Clues are sorted so their
order does not reveal which position matched.
"""

from __future__ import annotations

import random

NUM_DIGITS = 3
MAX_GUESSES = 10


def get_secret_num(rng: random.Random | None = None) -> str:
    """Return NUM_DIGITS unique digits, shuffled from 0-9."""
    numbers = list("0123456789")
    (rng or random).shuffle(numbers)
    return "".join(numbers[:NUM_DIGITS])


def is_valid_guess(guess: str) -> bool:
    return len(guess) == NUM_DIGITS and guess.isdecimal()


def get_clues(guess: str, secret_num: str) -> str:
    """Return the clue string for one guess against the secret."""
    if guess == secret_num:
        return "You got it!"

    clues: list[str] = []
    for i in range(len(guess)):
        if guess[i] == secret_num[i]:
            clues.append("Fermi")
        elif guess[i] in secret_num:
            clues.append("Pico")

    if not clues:
        return "Bagels"

    clues.sort()
    return " ".join(clues)
