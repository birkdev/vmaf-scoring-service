from fastapi import FastAPI, Request, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from tempfile import TemporaryDirectory
from pathlib import Path
from vmaf import vmaf
import shutil


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse(request, "index.html")


@app.post("/files")
async def score_files(reference: UploadFile, distorted: UploadFile):
    if reference.filename is None or distorted.filename is None:
        return {"error": "Filenames are required"}

    with TemporaryDirectory() as tmp_dir:
        ref_path = Path(tmp_dir) / reference.filename
        dist_path = Path(tmp_dir) / distorted.filename

        with open(ref_path, "wb") as f:
            shutil.copyfileobj(reference.file, f)

        with open(dist_path, "wb") as f:
            shutil.copyfileobj(distorted.file, f)

        score = vmaf(dist_path, ref_path)
        return {"vmaf_score": score}
