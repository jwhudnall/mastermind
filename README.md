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

## Additional Features

After satisfying the project requirements, I implemented the following additional features:

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

6. Popup modals for "How to Play", "New Game", and when the player either wins or loses.

   - Player Win:

     ![player-win](https://github.com/jwhudnall/mastermind/blob/main/static/images/readme-images/player-win-modal.png?raw=true)

   - Player Loss:

     ![player-loss](https://github.com/jwhudnall/mastermind/blob/main/static/images/readme-images/player-loss-modal.png?raw=true)

7. Python tests, testing core functionality and routes.

   - ![tests](https://github.com/jwhudnall/mastermind/blob/main/static/images/readme-images/running-tests.png?raw=true)

## Design Considerations

- Before starting, I created a Trello board to map out core functionality and features: [Trello Board](https://trello.com/b/efjqNs5f/mastermind)
- I decided to use Flask on the back-end due to my past experience, as well as given the fact that this project was completed with the goal of obtaining a back-end Software Engineering position. JQuery was used for quick prototyping.
- Early in the project I decided to adopt an OOP approach, implementing a `Mastermind` python class.
