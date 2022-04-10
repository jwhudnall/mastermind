"""Tests for Mastermind Routes."""

from unittest import TestCase
from models import Mastermind
import json

from app import app
app.config['TESTING'] = True

class RoutesTestCase(TestCase):
  """Test views for primary routes."""

  def setUp(self):
    self.client = app.test_client()

  def test_main_game_route(self):
    """Check main page containing gameboard."""

    with self.client as c:
      res = c.get('/')
      html = res.get_data(as_text=True)

      self.assertEqual(res.status_code, 200)
      self.assertIn("Remaining Guesses:", html)
      self.assertIn('<input type="number" id="num_cols" name="num_cols" min="4" max="8"', html)
      self.assertIn('<input type="number" id="num_rows" name="num_rows" min="1" max="15"', html)
      self.assertIn('<input type="number" id="num_colors" name="num_colors" min="2" max="8"', html)
      self.assertIn('<button>New Game</button>', html)
      self.assertIn('<input type="button" value="Submit" class="submitGuessBtn" id="row-', html)

  def test_api_guess_call_success(self):
    """Check guess call to the API for correctly-formatted guess."""

    with self.client as c:
      headers = { "content-type": "application/json" }
      data = json.dumps({"guess": ["1", "2", "3", "4"] })
      res = c.post('/api/guess', data=data, headers=headers)
      html = res.get_data(as_text=True)

      self.assertEqual(res.status_code, 200)
      self.assertTrue('colors' in res.json['game'])
      self.assertTrue('cols' in res.json['game'])
      self.assertTrue('current_guess' in res.json['game'])
      self.assertTrue('game_over' in res.json['game'])
      self.assertTrue('remaining_guess_count' in res.json['game'])
      self.assertTrue('rows' in res.json['game'])
      self.assertTrue('winning_sequence' in res.json['game'])

      self.assertTrue('blank' in res.json['results'])
      self.assertTrue('red' in res.json['results'])
      self.assertTrue('white' in res.json['results'])

  def test_api_guess_call_invalid_input(self):
    """Check guess call to the API for incorrectly-formatted guess (string not castable to int)."""

    with self.client as c:
      headers = { "content-type": "application/json" }
      data = json.dumps({"guess": ["1", "a", "3", "4"] })
      res = c.post('/api/guess', data=data, headers=headers)
      html = res.get_data(as_text=True)

      self.assertEqual(res.status_code, 400)
      self.assertTrue('castable to a number' in res.json['error'])

  def test_api_guess_call_invalid_input(self):
    """Check guess call to the API for incorrectly-formatted guess (value above specified limit)."""

    with self.client as c:
      headers = { "content-type": "application/json" }
      data = json.dumps({"guess": ["1", "12", "3", "4"] })
      res = c.post('/api/guess', data=data, headers=headers)
      html = res.get_data(as_text=True)

      self.assertEqual(res.status_code, 400)
      self.assertTrue('above or below' in res.json['error'])