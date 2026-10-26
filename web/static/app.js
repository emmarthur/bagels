const formEl = document.getElementById("guess-form");
const guessEl = document.getElementById("guess");
const guessesLeftEl = document.getElementById("guesses-left");
const errorEl = document.getElementById("error-text");
const bannerEl = document.getElementById("result-banner");
const historyEl = document.getElementById("history");
const historyEmptyEl = document.getElementById("history-empty");
const btnGuess = document.getElementById("btn-guess");
const btnNew = document.getElementById("btn-new");

let gameId = null;
let numDigits = 3;
let maxGuesses = 10;
let status = "playing";

function showError(message) {
  if (!message) {
    errorEl.hidden = true;
    errorEl.textContent = "";
    return;
  }
  errorEl.hidden = false;
  errorEl.textContent = message;
}

function apiDetail(data) {
  const detail = data?.detail;
  if (typeof detail === "string") return detail;
  if (Array.isArray(detail)) {
    return detail.map((item) => item.msg || String(item)).join(" ");
  }
  return "Request failed.";
}

function clueClass(clues) {
  if (clues === "You got it!") return "clue-win";
  if (clues === "Bagels") return "clue-bagels";
  if (clues.includes("Fermi")) return "clue-fermi";
  if (clues.includes("Pico")) return "clue-pico";
  return "";
}

function renderHistory(history) {
  historyEl.replaceChildren();
  for (const row of history) {
    const li = document.createElement("li");
    const num = document.createElement("span");
    num.className = "num";
    num.textContent = `#${row.guessNumber}`;

    const digits = document.createElement("span");
    digits.className = "digits";
    digits.textContent = row.guess;

    const clue = document.createElement("span");
    clue.className = `clue ${clueClass(row.clues)}`;
    clue.textContent = row.clues;

    li.append(num, digits, clue);
    historyEl.append(li);
  }
  historyEmptyEl.hidden = history.length > 0;
}

function applyState(data) {
  gameId = data.gameId;
  numDigits = data.numDigits;
  maxGuesses = data.maxGuesses;
  status = data.status;

  guessEl.maxLength = numDigits;
  guessEl.placeholder = "0".repeat(numDigits);

  renderHistory(data.history || []);

  if (status === "playing") {
    guessesLeftEl.textContent = `${data.guessesLeft} guess${data.guessesLeft === 1 ? "" : "es"} left`;
    bannerEl.hidden = true;
    guessEl.disabled = false;
    btnGuess.disabled = false;
  } else {
    guessEl.disabled = true;
    btnGuess.disabled = true;
    bannerEl.hidden = false;
    if (status === "won") {
      bannerEl.className = "banner is-win";
      bannerEl.textContent = "You got it!";
    } else {
      bannerEl.className = "banner is-loss";
      bannerEl.textContent = `Out of guesses. The number was ${data.answer}.`;
    }
    guessesLeftEl.textContent = "Round over";
  }
}

async function startGame() {
  showError("");
  bannerEl.hidden = true;
  guessEl.value = "";
  try {
    const res = await fetch("/api/games", { method: "POST" });
    const data = await res.json().catch(() => ({}));
    if (!res.ok) throw new Error(apiDetail(data));
    applyState(data);
    guessEl.focus();
  } catch (err) {
    showError(err.message || "Could not start a game.");
  }
}

async function submitGuess(event) {
  event.preventDefault();
  if (status !== "playing" || !gameId) return;
  showError("");

  const guess = guessEl.value.trim();
  if (guess.length !== numDigits || !/^\d+$/.test(guess)) {
    showError(`Enter exactly ${numDigits} digits.`);
    return;
  }

  try {
    const res = await fetch(`/api/games/${gameId}/guess`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ guess }),
    });
    const data = await res.json().catch(() => ({}));
    if (!res.ok) throw new Error(apiDetail(data));
    applyState(data);
    if (status === "playing") {
      guessEl.value = "";
      guessEl.focus();
    }
  } catch (err) {
    showError(err.message || "Could not submit guess.");
  }
}

formEl.addEventListener("submit", submitGuess);
btnNew.addEventListener("click", () => startGame());

document.querySelectorAll("[data-help-jump]").forEach((btn) => {
  btn.addEventListener("click", () => {
    document.getElementById("help-heading")?.scrollIntoView({
      behavior: "smooth",
      block: "start",
    });
  });
});

guessEl.addEventListener("input", () => {
  guessEl.value = guessEl.value.replace(/\D/g, "").slice(0, numDigits);
});

startGame();
