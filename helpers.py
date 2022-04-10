# Helper functions for Mastermind App
from flask import jsonify

def validate_guess_inputs(guess, game):
  '''Guess input validation. Checks if any values aren't castable to numbers, or are out of range Returns a JSON response with an error key indicating
  the first failed check, if present. If all guess inputs are valid, returns False.
  '''
  filtered = [n for n in guess if n != '']
  invalid_inputs = any(not val.lstrip("-").isdigit() for val in guess)

  try:
    not_in_range = any(int(val) < 0 or int(val) > game.colors - 1 for val in guess)
  except ValueError:
    return jsonify(error='One or more guess values wasn\'t castable to a number. Please use the gameboard to submit guesses.'), 400

  if len(filtered) != game.cols:
    # flash('Please submit a guess for each position in the row.')
    return jsonify(error='Guess values must equal Game columns.')
  elif invalid_inputs:
    # flash('One or more guess values were invalid. Please use the gameboard to submit guesses.')
    return jsonify(error='One or more guess values didn\'t cast to a number. Please use the gameboard to submit guesses.'), 400
  elif not_in_range:
    return jsonify(error='One or more guess values were above or below the specified game parameters. Please use the gameboard to submit guesses.'), 400
  return False
