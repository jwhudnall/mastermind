// Refactor out?
const submitGuessBtn = $(".submitGuessBtn");

const handleGuess = async function () {
  const inputs = $("[data-dropped]");
  const values = $.map(inputs, function (val) {
    return val.dataset.dropped;
  });
  const JSValues = $.makeArray(values);
  const res = await sendGuessToServer(JSValues);
  if (res) {
    const rowNum = res.game.current_guess - 1;
    provideFeedback(rowNum, res.results);
    disableRow(rowNum);
    const gameIsOver = checkForGameOver(res);
    if (!gameIsOver) {
      showNextRow(rowNum + 1);
      decrementGuessCount();
    }
  }
};

// Grab all droppables to isolate current row
// After a peg is dropped, add a data-selected attribute to the target

const sendGuessToServer = async function (guessList) {
  try {
    const res = await axios.post(
      "/api/guess",
      { guess: { guessList } },
      { headers: { "content-type": "application/json" } }
    );
    console.log(res.data);

    if (res.data.error) {
      alert("All inputs are required");
      return false;
    } else {
      console.log("Results:");
      console.log(res.data);
      return res.data;
    }
  } catch (e) {
    alert(`Something went wrong translating your guess. Error info: ${e}`);
  }
};

const provideFeedback = (curRow, res) => {
  let curPeg = 0;
  if (res.red) {
    for (let i = 0; i < res.red; i++) {
      const target = $(`#row${curRow}ResultPeg-${curPeg}`);
      target.attr("src", "/static/images/result-circle-red.png");
      console.log(`Result peg: ${curPeg} set to RED.`);
      curPeg++;
    }
  }
  if (res.white) {
    for (let i = 0; i < res.white; i++) {
      const target = $(`#row${curRow}ResultPeg-${curPeg}`);
      target.attr("src", "/static/images/result-circle-white.png");
      console.log(`Result peg: ${curPeg} set to WHITE.`);
      curPeg++;
    }
  }
};

const showNextRow = (row) => {
  $(`#row${row} td div`).each(function () {
    $(this).addClass("droppable");
  });
  // Add back event listeners for droppable
  $(".droppable").on("dragover", dragOver).off("drop", drop);
  $(`#row-${row}-Btn`).show();
  setListeners();
};

const disableRow = (curRow) => {
  curRow = parseInt(curRow);
  // Remove event listeners for droppable divs
  $(".droppable").unbind("dragover", dragOver);
  $(".droppable").unbind("drop", drop);

  $("[data-dropped]").each(function () {
    $(this).removeClass("dropped");
    $(this).removeClass("droppable");
    $(this).removeAttr("data-dropped");
  });
  $(`#row-${curRow}-Btn`).hide();
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

const handleGameLoss = () => {
  submitGuessBtn.prop("hidden", true);
  alert("Game Over. I'm sure you'll get it next time!");
};

const checkForGameOver = (res) => {
  if (res.game.game_over) {
    handleGameWin(res.game.winning_sequence);
    return true;
  } else if (res.game.remaining_guess_count === 0) {
    handleGameLoss();
    return true;
  }
  return false;
};

const showWinningSequence = (winningSequence) => {
  for (let i = 0; i < winningSequence.length; i++) {
    const value = winningSequence[i];
    $(`#actual-${i}`).fadeOut(function () {
      // $(this).text(value).fadeIn(1500);
      $(this)
        .css({ "background-image": `url('../static/images/guess-choices/peg${value}.gif')` })
        .fadeIn(1500);
    });
  }
};

submitGuessBtn.click(handleGuess);

// Drag Events TODO: Change to JQUERY
// const draggableElements = document.querySelectorAll(".draggable");
// const droppableElements = document.querySelectorAll(".droppable");

// draggableElements.forEach((el) => {
//   el.addEventListener("dragstart", dragStart);
// });

// droppableElements.forEach((el) => {
//   el.addEventListener("dragover", dragOver);
//   el.addEventListener("drop", drop);
// });
$(document).ready(function () {
  setListeners();
});

const removeListeners = () => {
  const draggableElements = document.querySelectorAll(".draggable");
  const droppableElements = document.querySelectorAll(".droppable");

  draggableElements.forEach((el) => {
    el.removeEventListener("dragstart", dragStart);
  });

  droppableElements.forEach((el) => {
    el.removeEventListener("dragover", dragOver);
    el.removeEventListener("drop", drop);
  });
};

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
  ev.dataTransfer.setData("text", ev.target.id);
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
