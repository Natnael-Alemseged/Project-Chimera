"""Core game logic for a small CLI 'Guess the Number' game.

Design goals:
- Small, testable Game class (no stdin/stdout) for unit tests
- Thin interactive wrapper in __main__.py
"""
from __future__ import annotations
import random
from typing import Optional

class Game:
    """Deterministic, testable game logic.

    Usage:
      g = Game(low=1, high=100, max_attempts=10, secret=42)
      result = g.guess(50)  # 'low' | 'high' | 'correct'
    """

    def __init__(self, low: int = 1, high: int = 100, *, max_attempts: Optional[int] = None, secret: Optional[int] = None):
        if low >= high:
            raise ValueError("low must be < high")
        self.low = int(low)
        self.high = int(high)
        self.secret = int(secret) if secret is not None else random.randint(self.low, self.high)
        self.attempts = 0
        self.max_attempts = int(max_attempts) if max_attempts is not None else max(5, (self.high - self.low) // 10 + 5)
        self.last_result: Optional[str] = None

    def guess(self, value: int) -> str:
        if not isinstance(value, int):
            raise TypeError("guess must be an int")
        if value < self.low or value > self.high:
            raise ValueError(f"guess must be between {self.low} and {self.high}")
        self.attempts += 1
        if value == self.secret:
            self.last_result = "correct"
        elif value < self.secret:
            self.last_result = "low"
        else:
            self.last_result = "high"
        return self.last_result

    def is_won(self) -> bool:
        return self.last_result == "correct"

    def is_over(self) -> bool:
        return self.is_won() or self.attempts >= self.max_attempts

    def reset(self, *, secret: Optional[int] = None) -> None:
        self.secret = int(secret) if secret is not None else random.randint(self.low, self.high)
        self.attempts = 0
        self.last_result = None
