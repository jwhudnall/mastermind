# Mastermind Game

https://user-images.githubusercontent.com/50386174/162826068-d80db855-11e0-44d7-967f-704d8b06a8de.mov

This is a code-breaking game where the user players a fictitious opponent. The "How to Play" modal explains it best: 
![How to Play Modal](https://github.com/jwhudnall/mastermind/blob/main/static/images/readme-images/how-to-play.png?raw=true)

## Getting Started
To run the game, you should have the latest version of [Python](https://www.python.org/downloads/) installed (including pip), as well as [git](https://git-scm.com/downloads).

1. From the command line, clone the Mastermind codebase to your preferred location by running: `git clone https://github.com/jwhudnall/mastermind.git`.
2. (Recommended) Within the cloned folder, create a virtual environment using `venv`. From the command line, navigate to your desired location and run: `python -m venv venv`.

   - **Mac Users:** Activate this environment by running: `source venv/bin/activate`.
   - **Windows Users:** Activate this environment by running: `source venv/Scripts/activate`.

   When you're done, you can deactivate the environment via `deactivate`.

3. If you're using a virtual environment, ensure that it is active before proceeding. Install the dependencies via `pip install -r requirements.txt`.
4. Tests can be run from the command line via `python -m unittest`. 5. Start the game via `flask run`. (If you wish to use an alternate port, run `flask run -p desired_port`). 6. In your browser, copy/paste the following link: `localhost:5002` (where _5002_ is the port specified after initiating `flask run`).

## Gameplay

- Explain the game
- Video Link: https://youtu.be/nXwe7Sl5eTo

## Additional Features

- Dynamic gameboard
- Colored Pegs (playing pieces)
- Colored Pegs (guess feedback)

## Design Considerations

- Link trello board
- Explain check_guess logic
- Explain Mastermind OOP
- Explain Flask, jQuery decision?
