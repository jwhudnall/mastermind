from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/')
def display_game():
  res = get_numbers()
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



# Helper Functions
def check_guess(actual, guess):
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
      actual_copy[i].pop(i)
      guess_copy.pop(i)

  for i in range(len(guess_copy)):
    if guess[i] in actual_copy:
      key['correct_num'] = key['correct_num'] + 1
      actual_copy[i] = None
      guess_copy[i] = None
    else:
      key['incorrect'] = key['incorrect'] + 1

  return key



def get_numbers():
  '''
  Retrieves random numbers from the random.org api.
  '''
  base_url = 'https://www.random.org/integers/'
  params = {
    'num': 4,
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
  print(f'Numbers: {num_list}')
  # import pdb
  # pdb.set_trace()
  return num_list