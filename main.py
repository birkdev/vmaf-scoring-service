from fastapi import FastAPI, Request, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from tempfile import TemporaryDirectory
from pathlib import Path
from vmaf import vmaf
import shutil
import sqlite3


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

MAX_SIZE = 32 * 1024 * 1024


@app.get("/monitor", response_class=HTMLResponse)
async def monitor(request: Request):
    con = sqlite3.connect("data/monitor.db")
    con.row_factory = sqlite3.Row
    checks = con.execute("SELECT * FROM checks ORDER BY id DESC LIMIT 100").fetchall()
    con.close()
    return templates.TemplateResponse(request, "monitor.html", {"checks": checks})


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse(request, "index.html")


@app.post("/files")
async def score_files(reference: UploadFile, distorted: UploadFile):
    if reference.filename is None or distorted.filename is None:
        return {"error": "Filenames are required"}

    if reference.size is None or distorted.size is None:
        return {"error": "Empty file"}

    if reference.size > MAX_SIZE or distorted.size > MAX_SIZE:
        return {"error": "File too large. Maximum size is 32 MB."}

    with TemporaryDirectory() as tmp_dir:
        ref_path = Path(tmp_dir) / reference.filename
        dist_path = Path(tmp_dir) / distorted.filename

        with open(ref_path, "wb") as f:
            shutil.copyfileobj(reference.file, f)

        with open(dist_path, "wb") as f:
            shutil.copyfileobj(distorted.file, f)

        score = vmaf(dist_path, ref_path)
        return {"vmaf_score": score}
