from flask import Flask, render_template, request, jsonify, flash
from models import Mastermind

app = Flask(__name__)
game = Mastermind()

# prevent cached responses
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

@app.route('/', methods=['GET', 'POST'])
def display_game():
  '''
  Primary game route. Player-defined game parameters are received as POST requests,
  wherein the global game variable is updated.
  '''

  if request.method == 'GET':
    return render_template('index.html', game=game)
  else:
    global_list = globals()
    num_cols = int(request.form.get('num_cols', None))
    num_rows = int(request.form.get('num_rows', None))
    num_colors = int(request.form.get('num_colors', None))
    global_list['game'] =  Mastermind(rows=num_rows, cols=num_cols, colors=num_colors)
    return render_template('index.html', game=game)

@app.route("/api/guess", methods=["POST"])
def handle_guess():
  '''
  Receives and validates guess from the client.
  '''

  guess = request.json['guess']['guessList']
  response_if_invalid = game.validate_guess_inputs(guess)

  if response_if_invalid:
    return response_if_invalid
  else:
    results = game.check_guess(game.winning_sequence, guess)
    game.current_guess += 1
    game.remaining_guess_count -= 1
    if results['red'] == game.cols:
      game.game_over = True

    return jsonify({
      'results': results,
      'game': game.serialize()
      })

