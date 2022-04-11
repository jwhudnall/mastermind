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
            self.assertIn("Guesses:", html)
            self.assertIn('How to Play', html)
            self.assertIn('New Game', html)
            self.assertIn('Mastermind', html)

    def test_api_guess_call_success(self):
        """Check guess call to the API for correctly-formatted guess."""

        with self.client as c:
            headers = {"content-type": "application/json"}
            data = json.dumps({"guess": ["1", "2", "3", "4"]})
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
            headers = {"content-type": "application/json"}
            data = json.dumps({"guess": ["1", "a", "3", "4"]})
            res = c.post('/api/guess', data=data, headers=headers)
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 400)
            self.assertTrue('castable to a number' in res.json['error'])

    def test_api_guess_call_invalid_input(self):
        """Check guess call to the API for incorrectly-formatted guess (value above specified limit)."""

        with self.client as c:
            headers = {"content-type": "application/json"}
            data = json.dumps({"guess": ["1", "12", "3", "4"]})
            res = c.post('/api/guess', data=data, headers=headers)
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 400)
            self.assertTrue('above or below' in res.json['error'])
