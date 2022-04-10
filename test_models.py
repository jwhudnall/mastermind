from models import Mastermind
from unittest import TestCase

class TestHelperFunctions(TestCase):
    """Tests helper functions."""

    def test_mastermind_model_default(self):
      """Tests Mastermind game class initialized as with default parameters."""
      game = Mastermind()
      serialized = game.serialize()

      self.assertEqual(game.cols, 4)
      self.assertEqual(game.rows, 10)
      self.assertEqual(len(game.winning_sequence), game.cols)
      self.assertEqual(game.remaining_guess_count, game.rows)
      self.assertEqual(game.current_guess, 1)
      self.assertFalse(game.game_over)
      self.assertEqual(serialized, {
        "rows": game.rows,
        "cols": game.cols,
        "winning_sequence": game.winning_sequence,
        "remaining_guess_count": game.remaining_guess_count,
        "current_guess": game.current_guess,
        "game_over": game.game_over,
        "colors": 8
      })

    def test_mastermind_validate_guess_inputs(self):
      """Tests Mastermind validate_guess_inputs method."""
      game = Mastermind()

      non_int_validation = game.validate_guess_inputs(['1','invalid', '3', '4'])
      self.assertTrue('wasn\'t castable to a number' in non_int_validation['error'])

      below_threshold_validation = game.validate_guess_inputs(['1','-3', '3', '4'])
      self.assertTrue('above or below the specified game parameters' in below_threshold_validation['error'])

      above_threshold_validation = game.validate_guess_inputs(['1','12', '3', '4'])
      self.assertTrue('above or below the specified game parameters' in above_threshold_validation['error'])

      above_col_threshold_validation = game.validate_guess_inputs(['1','2', '3', '4', '5'])
      self.assertTrue('values must equal Game' in above_col_threshold_validation['error'])

      below_col_threshold_validation = game.validate_guess_inputs(['1','2', '3'])
      self.assertTrue('values must equal Game' in below_col_threshold_validation['error'])


    def test_mastermind_model_modified(self):
      """Tests Mastermind game class initialized as with default parameters."""
      game = Mastermind(rows=8, cols=6, colors=4)
      serialized = game.serialize()

      self.assertEqual(game.cols, 6)
      self.assertEqual(game.rows, 8)
      self.assertEqual(len(game.winning_sequence), game.cols)
      self.assertEqual(game.remaining_guess_count, game.rows)
      self.assertEqual(game.current_guess, 1)
      self.assertFalse(game.game_over)
      self.assertEqual(serialized, {
        "rows": game.rows,
        "cols": game.cols,
        "winning_sequence": game.winning_sequence,
        "remaining_guess_count": game.remaining_guess_count,
        "current_guess": game.current_guess,
        "game_over": game.game_over,
        "colors":4
      })

    def test_mastermind_check_guess(self):
      """Tests Mastermind check_guess(actual, guess) classmethod."""
      self.assertEqual(Mastermind.check_guess(
        ['1','2','3','4'],
        ['1','2','3','4']
        ), {'white': 0, 'red': 4,'blank': 0
      })
      self.assertEqual(Mastermind.check_guess(
        ['1','2','3','4'],
        ['4','3','2','1']
        ), {'white': 4, 'red': 0,'blank': 0
      })
      self.assertEqual(Mastermind.check_guess(
        ['1','2','3','4'],
        ['2','2','1','5']
        ), {'white': 1, 'red': 1,'blank': 2
      })
      self.assertEqual(Mastermind.check_guess(
        ['1','2','3','4'],
        ['5','5','5','5']
        ), {'white': 0, 'red': 0,'blank': 4
      })