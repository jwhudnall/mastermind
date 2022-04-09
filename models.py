###################
# Primary Game Class
###################
import requests

class Mastermind:
  def __init__(self, rows=10, cols=4, colors=8):
    '''Mastermind Game class.'''
    self.rows = rows
    self.cols = cols
    self.colors = colors
    self.winning_sequence = Mastermind.get_numbers(count=self.cols,max=self.colors - 1)
    self.remaining_guess_count = rows
    self.current_guess = 1
    self.game_over = False

  def __repr__(self):
    return f'<Mastermind rows={self.rows} cols={self.cols}>'

  def serialize(self):
    return {
      "rows": self.rows,
      "cols": self.cols,
      "winning_sequence": self.winning_sequence,
      "remaining_guess_count": self.remaining_guess_count,
      "current_guess": self.current_guess,
      "game_over": self.game_over
      }

  @classmethod
  def get_numbers(self, count, max):
    '''
    Retrieves random numbers from the random.org api.
    '''
    base_url = 'https://www.random.org/integers/'
    params = {
      'num': count,
      'min':0,
      'max':max,
      'col':1,
      'base':10,
      'format': 'plain',
      'rnd':'new'
    }

    res = requests.get(f'{base_url}', params=params)
    text = res.text
    num_list = text.split('\n')[0:-1] # list of numbers, as strings
    return num_list

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