###################
# Primary Game Class
###################
import requests
from flask import jsonify


class Mastermind:
    def __init__(self, rows=10, cols=4, colors=8):
        '''Mastermind Game class.'''
        self.rows = rows
        self.cols = cols
        self.colors = colors
        self.winning_sequence = Mastermind.get_numbers(
            count=self.cols, max=self.colors - 1)
        self.remaining_guess_count = rows
        self.current_guess = 1
        self.game_over = False

    def __repr__(self):
        return f'<Mastermind rows={self.rows} cols={self.cols}>'

    def serialize(self):
        return {
            'rows': self.rows,
            'cols': self.cols,
            'winning_sequence': self.winning_sequence,
            'remaining_guess_count': self.remaining_guess_count,
            'current_guess': self.current_guess,
            'colors': self.colors,
            'game_over': self.game_over
        }

    @classmethod
    def get_numbers(self, count, max):
        '''
        Retrieves random numbers from the random.org api.
        '''
        base_url = 'https://www.random.org/integers/'
        params = {
            'num': count,
            'min': 0,
            'max': max,
            'col': 1,
            'base': 10,
            'format': 'plain',
            'rnd': 'new'
        }

        res = requests.get(f'{base_url}', params=params)
        text = res.text
        num_list = text.split('\n')[0:-1]  # list of numbers, as strings
        return num_list

    @classmethod
    def check_guess(self, actual, guess):
        '''Compares each value in the actual, guess lists for equality. Returns feedback'''
        key = {
            'white': 0,
            'red': 0,
            'blank': 0
        }
        actual_copy = actual[:]
        guess_copy = guess[:]

        for i in range(len(guess)):
            if guess[i] == actual[i]:
                key['red'] = key['red'] + 1
                # Remove for later inclusion check
                actual_copy[i] = None
                guess_copy[i] = None

        for i in range(len(guess_copy)):
            cur_val = guess_copy[i]
            if cur_val != None and cur_val in actual_copy:
                key['white'] = key['white'] + 1
                # Set index of value in actual_copy to None
                idx = actual_copy.index(cur_val)
                actual_copy[idx] = None
            elif cur_val != None:
                key['blank'] = key['blank'] + 1

        return key

    def validate_guess_inputs(self, guess):
        '''Input validation. Returns error dict if invalid, else False.

        Checks if any values aren't castable to numbers, or are out of range Returns a JSON response with an error key indicating the first failed check, if present. If all guess inputs are valid, returns False.

        Accepts:
            - guess: List of numerical strings (ex: [['1','2','3','4']])
            - game: Mastermind Class instance.
        Returns:
            - False if validation passes, else JSON response with error key indicating issue.
        '''

        guess_blanks_removed = [n for n in guess if n != '']

        try:
            not_in_range = any(int(val) < 0 or int(
                val) > self.colors - 1 for val in guess)
        except ValueError:
            return {'error': 'One or more guess values wasn\'t castable to a number.'}

        if len(guess_blanks_removed) != self.cols:
            return {'error': 'Guess values must equal Game columns.'}
        elif not_in_range:
            return {'error': 'One or more guess values were above or below the specified game parameters.'}
        else:
            return False
