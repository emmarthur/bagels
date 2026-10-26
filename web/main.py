"""
FastAPI app — Bagels.

Endpoints:
  GET  /                      HTML UI
  POST /api/games             Start a game
  POST /api/games/{id}/guess  Submit one guess

Run: uvicorn main:app --reload --port 3014
"""

from __future__ import annotations

import sys
import uuid
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

_DEMO_ROOT = Path(__file__).resolve().parent.parent
if str(_DEMO_ROOT) not in sys.path:
    sys.path.insert(0, str(_DEMO_ROOT))

from bagels_core import (  # noqa: E402
    MAX_GUESSES,
    NUM_DIGITS,
    get_clues,
    get_secret_num,
    is_valid_guess,
)

app = FastAPI(title="Bagels")
templates = Jinja2Templates(directory=str(Path(__file__).parent / "templates"))
app.mount("/static", StaticFiles(directory=str(Path(__file__).parent / "static")), name="static")


class Game(BaseModel):
    secret: str
    history: list[dict[str, str | int]] = Field(default_factory=list)
    status: str = "playing"


class GuessRequest(BaseModel):
    guess: str = Field(..., max_length=16)


GAMES: dict[str, Game] = {}


def _public_state(game_id: str, game: Game, latest: dict | None = None) -> dict:
    payload = {
        "gameId": game_id,
        "numDigits": NUM_DIGITS,
        "maxGuesses": MAX_GUESSES,
        "guessesUsed": len(game.history),
        "guessesLeft": MAX_GUESSES - len(game.history),
        "status": game.status,
        "history": game.history,
        "answer": game.secret if game.status != "playing" else None,
    }
    if latest is not None:
        payload["latest"] = latest
    return payload


@app.get("/", response_class=HTMLResponse)
async def index(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        request,
        "index.html",
        {"num_digits": NUM_DIGITS, "max_guesses": MAX_GUESSES},
    )


@app.post("/api/games")
async def new_game() -> JSONResponse:
    game_id = uuid.uuid4().hex
    GAMES[game_id] = Game(secret=get_secret_num())
    return JSONResponse(_public_state(game_id, GAMES[game_id]))


@app.post("/api/games/{game_id}/guess")
async def submit_guess(game_id: str, body: GuessRequest) -> JSONResponse:
    game = GAMES.get(game_id)
    if game is None:
        raise HTTPException(status_code=404, detail="That game is not on this server. Start a new one.")
    if game.status != "playing":
        raise HTTPException(status_code=400, detail="This game is already over.")

    guess = body.guess.strip()
    if not is_valid_guess(guess):
        raise HTTPException(
            status_code=400,
            detail=f"Enter exactly {NUM_DIGITS} digits.",
        )

    clues = get_clues(guess, game.secret)
    guess_number = len(game.history) + 1
    game.history.append({"guess": guess, "clues": clues, "guessNumber": guess_number})

    if guess == game.secret:
        game.status = "won"
    elif guess_number >= MAX_GUESSES:
        game.status = "lost"

    latest = {"guess": guess, "clues": clues, "guessNumber": guess_number}
    return JSONResponse(_public_state(game_id, game, latest))
