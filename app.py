from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

###################
# OOP / Game Class
###################
class Mastermind:
  def __init__(self, rows=10, cols=4):
    '''Mastermind Game class.'''
    self.rows = rows
    self.cols = cols
    self.winning_numbers = Mastermind.get_numbers(self.cols)
    self.remaining_guess_count = rows
    self.current_guess = 0
    self.game_over = False

  def __repr__(self):
    return f'<Mastermind rows={self.rows} cols={self.cols}>'

  @classmethod
  def get_numbers(self, count=4):
    '''
    Retrieves random numbers from the random.org api.
    '''
    base_url = 'https://www.random.org/integers/'
    params = {
      'num': count,
      'min':0,
      'max':7,
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

game = Mastermind()
print(game.winning_numbers)

#############
# Main Routes
#############

@app.route('/')
def display_game():
  # TODO: Pass game to route and dynamically render the game board using jinja
  return render_template('index.html')

@app.route("/api/guess", methods=["POST"])
def handle_guess():
  '''
  Receives and validates guess from the client.
  '''
  guess = request.json['guess']['guessList']
  filtered = [n for n in guess if n != '']

  if (len(filtered) != game.cols):
    return jsonify(error='Guess values must equal Game columns.')
  else:
    results = game.check_guess(game.winning_numbers, guess)
    game.current_guess += 1
    game.remaining_guess_count -= 1
    if results['red'] == 4:
      game.game_over = True

    return jsonify({
      'results': results,
      'game_over':game.game_over,
      'current_guess': game.current_guess,
      'remaining_guess_count': game.remaining_guess_count
      })

