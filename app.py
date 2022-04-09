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
    self.winning_sequence = Mastermind.get_numbers(self.cols)
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

# game = Mastermind()
game = Mastermind()
# print(game.winning_sequence)

#############
# Main Routes
#############

@app.route('/', methods=['GET', 'POST'])
def display_game():
  if request.method == 'GET':
    return render_template('index.html', game=game)
  else:
    global_list = globals()
    num_cols = int(request.form.get('num_cols', None))
    num_rows = int(request.form.get('num_rows', None))
    global_list['game'] =  Mastermind(rows=num_rows, cols=num_cols)
    print(f'New game instantiated! Nums: {game.winning_sequence}')
    return render_template('index.html', game=game)


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
    results = game.check_guess(game.winning_sequence, guess)
    game.current_guess += 1
    game.remaining_guess_count -= 1
    if results['red'] == game.cols:
      game.game_over = True

    return jsonify({
      'results': results,
      'game_over':game.game_over,
      'current_guess': game.current_guess,
      'remaining_guess_count': game.remaining_guess_count,
      'game': game.serialize()
      })

