"""Interactive CLI wrapper for the guess-the-number game."""
from .game import Game
import argparse

RANGES = {
    "easy": (1, 10, 5),
    "medium": (1, 100, 10),
    "hard": (1, 1000, 15),
}


def play(difficulty: str = "medium", seed: int | None = None) -> None:
    low, high, attempts = RANGES.get(difficulty, RANGES["medium"])
    if seed is not None:
        import random

        random.seed(seed)

    g = Game(low, high, max_attempts=attempts)
    print(f"Guess the number between {low} and {high} — difficulty: {difficulty}")

    while not g.is_over():
        prompt = f"Attempt {g.attempts+1}/{g.max_attempts} — your guess (or 'q' to quit): "
        s = input(prompt).strip()
        if s.lower() in ("q", "quit", "exit"):
            print("Goodbye.")
            return
        try:
            n = int(s)
        except ValueError:
            print("Please enter an integer.")
            continue
        try:
            res = g.guess(n)
        except ValueError:
            print(f"Please enter a number between {low} and {high}.")
            continue
        if res == "correct":
            print(f"🎉 Correct! You found it in {g.attempts} attempts.")
            return
        print("Too low." if res == "low" else "Too high.")

    print(f"Game over — the number was {g.secret}.")


if __name__ == "__main__":
    p = argparse.ArgumentParser(prog="python -m cli_game", description="Play a small guess-the-number game in your terminal")
    p.add_argument("-d", "--difficulty", choices=["easy", "medium", "hard"], default="medium")
    p.add_argument("--seed", type=int, default=None, help="set RNG seed (useful for testing)")
    args = p.parse_args()
    play(args.difficulty, args.seed)
