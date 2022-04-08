// const row10Vals = $("#row10 td div input");
const submitGuessBtn = $(".submitGuessBtn");

// submitGuessBtn.click(async function () {
//   const rowNum = parseInt(this.id.split("-")[1]);
//   const inputs = $(`#row${rowNum} td div input`);
//   const values = $.map(inputs, function (val) {
//     return val.value;
//   });
//   const JSValues = $.makeArray(values);
//   const res = await sendGuessToServer(JSValues);
//   if (res) {
//     provideFeedback(rowNum, res.results);
//     disableRow(rowNum);
//     checkForGameOver(res);
//     showNextRow(rowNum + 1);
//     decrementGuessCount();
//   }
// });

const handleGuess = async function () {
  const rowNum = parseInt(this.id.split("-")[1]);
  const inputs = $(`#row${rowNum} td div input`);
  const values = $.map(inputs, function (val) {
    return val.value;
  });
  const JSValues = $.makeArray(values);
  const res = await sendGuessToServer(JSValues);
  if (res) {
    provideFeedback(rowNum, res.results);
    disableRow(rowNum);
    const gameIsOver = checkForGameOver(res);
    if (!gameIsOver) {
      showNextRow(rowNum + 1);
      decrementGuessCount();
    }
  }
};

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
  const inputs = $(`#row${row} td div input`);
  inputs.each(function () {
    $(this).prop("disabled", false);
  });
  $(`#row-${row}-Btn`).show();
};

const disableRow = (curRow) => {
  const currInputs = $(`#row${curRow} td div input`);

  currInputs.each(function () {
    $(this).prop("disabled", true);
  });
  $(`#row-${curRow}-Btn`).hide();
};

const decrementGuessCount = () => {
  const currentVal = parseInt($("#numGuessesLeft").text());
  $("#numGuessesLeft").text(currentVal - 1);
};

const handleGameWin = () => {
  submitGuessBtn.prop("hidden", true);
  alert("Congratulations, you win!");
};

const handleGameLoss = () => {
  submitGuessBtn.prop("hidden", true);
  alert("Game Over. I'm sure you'll get it next time!");
};

const checkForGameOver = (res) => {
  if (res.game.game_over) {
    handleGameWin();
    return true;
  } else if (res.game.remaining_guess_count === 0) {
    handleGameLoss();
    return true;
  }
  return false;
};

submitGuessBtn.click(handleGuess);
