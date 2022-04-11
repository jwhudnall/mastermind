$(document).ready(function () {
  setListeners();
  submitGuessBtn.click(handleGuess);
});

const submitGuessBtn = $(".submitGuessBtn");

const sendGuessToServer = async function (guess) {
  try {
    const res = await axios.post(
      "/api/guess",
      { guess },
      { headers: { "content-type": "application/json" } }
    );

    if (res.data.error) {
      alert("All inputs are required");
      return false;
    } else {
      // Uncomment to view response from console during game play:
      // console.log(res.data);
      return res.data;
    }
  } catch (e) {
    alert(`Something went wrong translating your guess. Error info: ${e}`);
  }
};

const handleGuess = async function () {
  const inputs = $("[data-dropped]");
  const values = $.map(inputs, function (val) {
    return val.dataset.dropped;
  });
  const res = await sendGuessToServer(values);
  if (res) {
    const rowNum = res.game.current_guess - 1;
    provideFeedback(rowNum, res.results);
    addTooltips("red", "white");
    disableRow(rowNum);
    const gameIsOver = checkForGameOver(res);
    if (!gameIsOver) {
      showNextRow(rowNum + 1);
      decrementGuessCount();
    }
  }
};

const provideFeedback = (curRow, res) => {
  let curPeg = 0;
  if (res.red) {
    for (let i = 0; i < res.red; i++) {
      const target = $(`#row${curRow}ResultPeg-${curPeg}`);
      target.attr("src", "/static/images/result-circle-red.png");
      target.attr("data-tooltip-target", "tooltip-red");
      // console.log(`Result peg: ${curPeg} set to RED.`);
      curPeg++;
    }
  }
  if (res.white) {
    for (let i = 0; i < res.white; i++) {
      const target = $(`#row${curRow}ResultPeg-${curPeg}`);
      target.attr("src", "/static/images/result-circle-white.png");
      // console.log(`Result peg: ${curPeg} set to WHITE.`);
      curPeg++;
    }
  }
};

const disableRow = (row) => {
  $("[data-dropped]").each(function () {
    $(this).removeClass("dropped");
    $(this).removeClass("droppable");
    $(this).removeAttr("data-dropped");
  });
  // $(`#row-${row}-Btn`).hide();
  $(`#row${row}`).removeClass("bg-slate-400");
};

const showNextRow = (row) => {
  $(`#row${row} td div`).each(function () {
    $(this).addClass("droppable");
  });
  // $(`#row-${row}-Btn`).show();
  $(`#row${row}`).addClass("bg-slate-400");
  setListeners();
};

const decrementGuessCount = () => {
  const currentVal = parseInt($("#numGuessesLeft").text());
  $("#numGuessesLeft").text(currentVal - 1);
};

const handleGameWin = (winningSequence) => {
  submitGuessBtn.prop("hidden", true);
  showWinningSequence(winningSequence);
  alert("Congratulations, you win!");
};

const handleGameLoss = (winningSequence) => {
  submitGuessBtn.prop("hidden", true);
  showWinningSequence(winningSequence);
  alert("Game Over. I'm sure you'll get it next time!");
};

const checkForGameOver = (res) => {
  if (res.game.game_over) {
    handleGameWin(res.game.winning_sequence);
    return true;
  } else if (res.game.remaining_guess_count === 0) {
    handleGameLoss(res.game.winning_sequence);
    return true;
  }
  return false;
};

const showWinningSequence = (winningSequence) => {
  for (let i = 0; i < winningSequence.length; i++) {
    const value = winningSequence[i];
    $(`#actual-${i}`).fadeOut(function () {
      $(this)
        .css({ "background-image": `url('../static/images/guess-choices/peg${value}.gif')` })
        .fadeIn(1500);
    });
  }
};

// *** Drag & Drop Functionality ***
const setListeners = () => {
  const draggableElements = document.querySelectorAll(".draggable");
  const droppableElements = document.querySelectorAll(".droppable");

  draggableElements.forEach((el) => {
    el.addEventListener("dragstart", dragStart);
  });

  droppableElements.forEach((el) => {
    el.addEventListener("dragover", dragOver);
    el.addEventListener("drop", drop);
  });
};

function dragStart(ev) {
  ev.dataTransfer.setData("text", ev.target.dataset.val);
}

function dragOver(e) {
  e.preventDefault();
}

// Drops peg into game slot, adding a data-attribute with the numerical value
function drop(ev) {
  ev.preventDefault();
  var data = ev.dataTransfer.getData("text");
  ev.target.style.backgroundImage = `url('../static/images/guess-choices/peg${data}.gif')`;
  ev.target.dataset.dropped = data;
}

//
/** Adds tooltip above result pegs.
 *  ex: addTooltips("red", "white") adds
 */
const addTooltips = function () {
  for (let color of arguments) {
    const targetEl = document.getElementById(`tooltip-${color}`);
    const triggerEls = document.querySelectorAll(
      `img[src$='/static/images/result-circle-${color}.png']`
    );
    triggerEls.forEach((el) => {
      new Tooltip(targetEl, el);
    });
  }
};
