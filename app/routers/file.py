from fastapi import FastAPI, Request, UploadFile, File, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from typing import List

IMAGEDIR = "images/"

router = FastAPI()
templates = Jinja2Templates(directory="templates")
router.mount("/images", StaticFiles(directory="images"), name="images")


@router.get('/', response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.post("/upload-files")
async def create_upload_files(request: Request, file: UploadFile = File(...)):
    contents = await file.read()
    # save the file
    with open(f"{IMAGEDIR}{file.filename}", "wb") as f:
        f.write(contents)

    show = file.filename

    # return {"Result": "OK", "filenames": [file.filename for file in files]}
    return templates.TemplateResponse("index.html", {"request": request, "show": show})