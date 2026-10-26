# Book directions — Bagels

**Catalog #436** · Al Sweigart, *The Big Book of Small Python Projects* — **Bagels**

- Local PDF: `E:\Books\career advancement\python\The Big Book of Small Python Projects 81 Easy Practice Programs (Al Sweigart) (z-lib.org).pdf`
- Online chapter: [inventwithpython.com/bigbookpython/project1.html](https://inventwithpython.com/bigbookpython/project1.html)
- Upstream: [bagels.py](https://github.com/asweigart/the-big-book-of-small-python-projects/blob/main/bagels.py)
- Shared logic: [`bagels_core.py`](./bagels_core.py)
- Terminal play: [`reference/bagels.py`](./reference/bagels.py)

## What the book asks you to build

1. Pick a secret of **3 unique digits** (`NUM_DIGITS = 3`) by shuffling `0`–`9` and taking the first three. The secret may start with `0`.
2. Allow **10 guesses** (`MAX_GUESSES = 10`).
3. A guess must be exactly 3 decimal digits. Repeated digits in the guess are allowed; only the secret is unique.
4. Clues, one per matching digit:
   - **Fermi** — digit is correct and in the right place.
   - **Pico** — digit is correct but in the wrong place.
   - **Bagels** — no digit is correct.
5. If the guess equals the secret, the clue is **You got it!**
6. Otherwise sort the clue words alphabetically and join them with spaces, so the order does not reveal which position matched. The book’s example: secret `248`, guess `843` → `Fermi Pico`.
7. After a win, or after 10 misses, the program can start another round. On a loss it reveals the secret.

## Web version (`web/` — FastAPI, port **3014**)

The secret stays on the server. The page sends each guess to `POST /api/games/{id}/guess` and shows the same clue string.

```powershell
Set-Location "c:\Users\emmak\Desktop\Content\CodingProjects\PortProjects\demos\bagels\web"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --port 3014
```
