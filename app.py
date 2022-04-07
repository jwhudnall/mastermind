from flask import Flask, render_template, request
import requests

app = Flask(__name__)


##################
# Helper Functions
##################



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
      'correct_num': 0,
      'correct_num_and_location': 0,
      'incorrect': 0
    }
    actual_copy = actual[:]
    guess_copy = guess[:]

    for i in range(len(guess)):
      if guess[i] == actual[i]:
        key['correct_num_and_location'] = key['correct_num_and_location'] + 1
        # Remove for later inclusion check
        actual_copy[i] = None
        guess_copy[i] = None

    for i in range(len(guess_copy)):
      cur_val = guess_copy[i]
      if cur_val != None and cur_val in actual_copy:
        key['correct_num'] = key['correct_num'] + 1
        # Set index of value in actual_copy to None
        idx = actual_copy.index(cur_val)
        actual_copy[idx] = None
      elif cur_val != None:
        key['incorrect'] = key['incorrect'] + 1

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

@app.route("/api/guess", methods=["GET"])
def handle_guess():
  '''
  Receives and validates guess from the client.
  '''
  # jQuery object list deconstructed: https://stackoverflow.com/questions/23889107/sending-array-data-with-jquery-and-flask
  guess = request.args.getlist('guessList[]')

  # Compare guess values vs. computer values
  # Return feedback
  results = game.check_guess(game.winning_numbers, guess)
  print(results)

  import pdb
  pdb.set_trace()
