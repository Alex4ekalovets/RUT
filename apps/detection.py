import logging
import os.path
from typing import List

from fastapi import FastAPI, Request, Response, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from utils.detection import detect_faces_and_save
from utils.image_tools import convert_image_to_bytes

logger = logging.getLogger("logger")

detection_app = FastAPI(title="Detection")

templates = Jinja2Templates(directory="templates")


class Filenames(BaseModel):
    filenames: list[str]


@detection_app.get("/", response_class=HTMLResponse)
async def detection(request: Request):
    return templates.TemplateResponse(request=request, name="detection.html")


@detection_app.get("/image/", response_class=Response)
async def get_image(name: str = "no_image.png"):
    image_bytes = convert_image_to_bytes(f"media/{name}")
    return Response(
        content=image_bytes,
        media_type="image/jpeg",
        headers={"Cache-Control": "no-store"},
    )


@detection_app.post("/uploadfile/")
async def upload_file(files: List[UploadFile]):
    for file in files:
        file_path = os.path.join("media", file.filename)
        with open(file_path, "wb") as image:
            image.write(file.file.read())
    return {"filenames": [file.filename for file in files]}


@detection_app.post("/face_detection")
async def face_detection(filenames: Filenames):
    filenames = filenames.dict()['filenames']
    file_paths = list(map(lambda x: os.path.join('media', x), filenames))
    new_filenames = detect_faces_and_save(images=file_paths, prefix='new_')
    return {"filenames": new_filenames}
