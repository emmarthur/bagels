# Bagels

Deduce a 3-digit number from Pico, Fermi, and Bagels clues. The secret stays on the server.

| Artifact | Path |
|----------|------|
| Book steps | [`BOOK_DIRECTIONS.md`](./BOOK_DIRECTIONS.md) |
| Shared logic | [`bagels_core.py`](./bagels_core.py) |
| Web (FastAPI) | [`web/`](./web/) — port **3014** |

## Run the web demo

```powershell
Set-Location "c:\Users\emmak\Desktop\Content\CodingProjects\PortProjects\demos\bagels\web"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --port 3014
```

Open [http://127.0.0.1:3014/](http://127.0.0.1:3014/).

## Run the terminal version

```powershell
Set-Location "c:\Users\emmak\Desktop\Content\CodingProjects\PortProjects\demos\bagels"
python reference\bagels.py
```
