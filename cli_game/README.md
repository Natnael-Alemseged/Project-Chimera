CLI Guess-the-number game (minimal)

Run locally:

  python -m cli_game

Options:
  -d/--difficulty  easy|medium|hard  (default: medium)
  --seed <int>     deterministic secret (useful for testing)

Run tests (uses stdlib unittest):

  python -m unittest discover -s cli_game/tests -p "test_*.py" -v

Ideas for improvements: leaderboard, configurable ranges, nicer CLI UX.
