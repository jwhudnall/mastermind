const row10Vals = $("#row10 td div input");
const row10Btn = $("#row10Btn");

row10Btn.click(() => {
  const values = $.map(row10Vals, function (val) {
    return val.value;
  });
  console.log(typeof values);
  const JSValues = $.makeArray(values);
  sendGuessToServer(JSValues);
});

const sendGuessToServer = async function (guessList) {
  try {
    const res = await axios.get("/api/guess", { params: { guessList } });
    console.log(res.data);

    if (res.data.error) {
      alert("All inputs are required");
    } else {
      provideFeedback(10, res);
      // Disable this row and traverse up the guess list.
      disableRow(10);
    }
  } catch (e) {
    alert(`Something went wrong translating your guess. Error info: ${e}`);
  }
};

const provideFeedback = (curRow, res) => {
  let curPeg = 0;
  if (res.data.red) {
    for (let i = 0; i < res.data.red; i++) {
      // Set ID of the curPeg to an image having a red circle background
      const target = $(`#row${curRow}ResultPeg-${curPeg}`);
      target.attr("src", "/static/images/result-circle-red.png");
      console.log(`Result peg: ${curPeg} set to RED.`);
      curPeg++;
    }
  }
  if (res.data.white) {
    for (let i = 0; i < res.data.white; i++) {
      const target = $(`#row${curRow}ResultPeg-${curPeg}`);
      target.attr("src", "/static/images/result-circle-white.png");
      console.log(`Result peg: ${curPeg} set to WHITE.`);
      curPeg++;
    }
  }
};

const disableRow = (curRow) => {
  const inputs = $(`#row${curRow} td div input`);

  inputs.each(function (i, el) {
    $(this).prop("disabled", true);
  });
  $(`#row${curRow}Btn`).hide();
};
