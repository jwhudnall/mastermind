# Mastermind Game

https://user-images.githubusercontent.com/50386174/162826068-d80db855-11e0-44d7-967f-704d8b06a8de.mov

This is a code-breaking game where the user plays a fictitious opponent. The "How to Play" modal explains it best:
![How to Play Modal](https://github.com/jwhudnall/mastermind/blob/main/static/images/readme-images/how-to-play.png?raw=true)

## Getting Started

To run the game, you should have the latest version of [Python](https://www.python.org/downloads/) installed (including pip), as well as [git](https://git-scm.com/downloads).

1. From the command line, clone the Mastermind codebase to your preferred location by running: `git clone https://github.com/jwhudnall/mastermind.git`.
2. (Recommended) Within the cloned folder, create a virtual environment using `venv`. From the command line, navigate to your desired location and run: `python -m venv venv`.

   - **Mac Users:** Activate this environment by running: `source venv/bin/activate`.
   - **Windows Users:** Activate this environment by running: `source venv/Scripts/activate`.

   When you're done, you can deactivate the environment via `deactivate`.

3. If you're using a virtual environment, ensure that it is active before proceeding. Install the dependencies via `pip install -r requirements.txt`.
4. Tests can be run from the command line via `python -m unittest`.
5. Start the game via `flask run`. (If you wish to use an alternate port, run `flask run -p desired_port`).
6. In your browser, copy/paste the following link: `localhost:5002` (where _5002_ is the port specified after initiating `flask run`).

## Game Logic Flow

Primary game logic is as follows:

1. The player is presented with an empty game board, with the first row highlighted (and identified via a left-facing arrow icon) to indicate the current row.

2. As the player drags and drops pegs onto the current row, the `data-val` attribute from the dragged piece translates into a `data-dropped` attribute on the game board slot.

3. When the player clicks the **Submit Guess** button, Javascript checks the values of each `data-dropped` value in the current row. If the length of these values is less than the current game's sequence length, a popup is displayed requesting that the user fills all row slots prior to submitting a guess.

4. The values from the JS array are sent to the server via a `POST` request. The guess is then validated server side, verifying that the values are of the correct length, data type and within the range of the specified `game.colors` value. In the unlikely event that this validation fails, the user is alerted via a JSON response containing an `error` key.

5. If the guess passes validation, it is then run through a `check_guess` function which compares the user-guess vs. the correct sequence. To accomplish this, I check the values in each array, first looking for cross-pairs (a correct guess in the correct position), and then inclusion in the solution array (cross-pairs matches are eliminated by setting them to None when matches occur in the previous step). The function returns a key containing `red`, `white` and `blank` key, value pairs.

6. The current game instance is then updated to account for the user guess. If all results are `red`, `game.game_over` is set to `True` (red values are compared to `game.cols`). The response is then JSONified and sent back to the client as a JSON object containing `results` and `game` keys.

7. On the front end, `provideFeedback` is called to fill in result peg slots, based on the `red` and `white` values from the response. To keep feedback uniform (and not indicate exactly which peg relates to the piece of feedback), red pegs are filled in, followed by white. Any blank values are ignored, as they are already indicated by the empty slots.

8. `addTooltips` is called to add tooltips atop the red and white result pegs, assisting the user in the event they forget how the feedback works.

9. `disableRow` then removes drop-related classes from the row that was used, and hides that row's arrow icon.

10. `checkForGameOver` is called to check the status of `game.game_over` and `game.remaining_guess_count` from the response. If either case is True, the appropriate popup is displayed, and the user is encouraged to play again. If not, `False` is returned in the `gameIsOver` variable that called the function.

11. `updateGuessCount` is then called to update the remaining guesses, as well as the elapsed guess count on the front end.

12. Finally, if `!gameIsOver` evaluates to True, `showNextRow` is called to add the appropriate drop classes to the next row, and show it's arrow icon. The game continues until either the player guesses the right sequence, or runs out of guesses.

## Additional Features

After satisfying the baseline project requirements, I implemented the following additional features:

1. Dynamic gameboard configuration to increase/decrease game difficulty. By clicking the **New Game** button, users can specify the code sequence length (columns), guess attempts (rows), and the available colors count:

   ![configurable-difficulty](https://github.com/jwhudnall/mastermind/blob/main/static/images/readme-images/configurable-difficulty.png?raw=true)

2. I refactored to use draggable, colored pegs instead of numbers. The core Random Number API is still used, wherein numbers are translated into colors.
3. Guess feedback in the form of red and white colored pegs, emulating the real Mastermind game. These are dynamically rendered using Jinja to match the current game's sequence length.
4. Tooltips were added above feedback pegs. When a user hovers over the red or white pegs, they are reminded of their significance:

   ![Tooltips](https://github.com/jwhudnall/mastermind/blob/main/static/images/readme-images/tooltips.png?raw=true)

5. Detailed API response for the `/api/guess` route, testable in Insomnia/Postman/curl (note: a `content-type: application/json` header must be set ). Depending on the POST request's content, the API will return either the requested data, or an error message indicating the issue:

   - Success:
     ![success](https://github.com/jwhudnall/mastermind/blob/main/static/images/readme-images/api-success.png?raw=true)

   - Value out of Range:
     ![out-of-range](https://github.com/jwhudnall/mastermind/blob/main/static/images/readme-images/api-char-out-of-range.png?raw=true)

   - Invalid value:
     ![invalid-character](https://github.com/jwhudnall/mastermind/blob/main/static/images/readme-images/api-invalid-char.png?raw=true)

   - Invalid length:
     ![invalid-character](https://github.com/jwhudnall/mastermind/blob/main/static/images/readme-images/api-invalid-length.png?raw=true)

6. Popup modals for "How to Play", "New Game", and when the player either wins or loses.

   - How to Play:

     ![how-to-play](https://github.com/jwhudnall/mastermind/blob/main/static/images/readme-images/how-to-play.png?raw=true)

   - New Game:

     ![new-game](https://github.com/jwhudnall/mastermind/blob/main/static/images/readme-images/new-game-modal.png?raw=true)

   - Player Win:

     ![player-win](https://github.com/jwhudnall/mastermind/blob/main/static/images/readme-images/player-win-modal.png?raw=true)

   - Player Loss:

     ![player-loss](https://github.com/jwhudnall/mastermind/blob/main/static/images/readme-images/player-loss-modal.png?raw=true)

7. Python tests, testing core functionality and routes:

   - ![tests](https://github.com/jwhudnall/mastermind/blob/main/static/images/readme-images/running-tests.png?raw=true)

## Design Considerations

- Before starting, I created a Trello board to map out core functionality and features: [Trello Board](https://trello.com/b/efjqNs5f/mastermind)

- I decided to use Flask on the back-end due to my past experience, as well as given the fact that this project was completed with the goal of obtaining a back-end Software Engineering position. JQuery was used for quick prototyping.

- Early in the project I decided to adopt an OOP approach, implementing a `Mastermind` python class.

- I landed on an implementation that didn't use cookies or localStorage. Game updates between guesses are conveyed via the `/api/guess` route response.

- Additional Features I wanted to implement, but ran out of time:
  - Hint feature.
  - Utilize localStorage for high scores
  - Implement time aspect (perhaps tied to scores)
  - Disallow the dropping of pieces in previous rows.
  - Add Javascript tests.
  - Edge Case handling: In the event the Random number API fails, I could easily add a python-based random number generator.
