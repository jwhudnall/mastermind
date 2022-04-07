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
    return res.data;
  } catch (e) {
    alert(`Something went wrong translating your guess. Error info: ${e}`);
  }
};
