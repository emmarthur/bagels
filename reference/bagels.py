"""Play Bagels in the terminal. The secret stays in this process."""

from bagels_core import MAX_GUESSES, NUM_DIGITS, get_clues, get_secret_num, is_valid_guess


def main() -> None:
    print(
        f"I am thinking of a {NUM_DIGITS}-digit number with no repeated digits.\n"
        f"You have {MAX_GUESSES} guesses.\n"
        "Pico  — one digit is correct but in the wrong position.\n"
        "Fermi — one digit is correct and in the right position.\n"
        "Bagels — no digit is correct.\n"
    )
    while True:
        secret = get_secret_num()
        print("I have thought up a number.")
        for num_guess in range(1, MAX_GUESSES + 1):
            guess = ""
            while not is_valid_guess(guess):
                guess = input(f"Guess #{num_guess}: ").strip()
            print(get_clues(guess, secret))
            if guess == secret:
                break
        else:
            print("You ran out of guesses.")
            print(f"The answer was {secret}.")

        again = input("Play again? (yes or no) ").strip().lower()
        if not again.startswith("y"):
            break
    print("Thanks for playing!")


if __name__ == "__main__":
    main()
