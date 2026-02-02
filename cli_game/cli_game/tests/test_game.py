import unittest

from cli_game.game import Game


class TestGame(unittest.TestCase):

    def test_correct_guess(self):
        g = Game(1, 10, max_attempts=5, secret=7)
        res = g.guess(7)
        self.assertEqual(res, "correct")
        self.assertTrue(g.is_won())
        self.assertTrue(g.is_over())

    def test_low_and_high(self):
        g = Game(1, 10, max_attempts=5, secret=5)
        self.assertEqual(g.guess(3), "low")
        self.assertFalse(g.is_won())
        self.assertEqual(g.guess(9), "high")
        self.assertFalse(g.is_won())

    def test_attempts_and_game_over(self):
        g = Game(1, 3, max_attempts=2, secret=1)
        self.assertEqual(g.guess(2), "high")
        self.assertFalse(g.is_over())
        self.assertEqual(g.guess(3), "high")
        self.assertTrue(g.is_over())


if __name__ == "__main__":
    unittest.main()
