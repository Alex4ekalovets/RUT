import logging
import os.path

from fastapi import FastAPI, Request, Response, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from starlette.responses import FileResponse

from utils.image_tools import image_handler, convert_image_to_bytes, get_image_size

logger = logging.getLogger("logger")

image_tools_app = FastAPI(title="Image Tools")

templates = Jinja2Templates(directory="templates")


class Rotate(BaseModel):
    angle: int


class Resize(BaseModel):
    width: int
    height: int
    save_ratio: bool = False
    side: str = None


class Crop(BaseModel):
    top: int
    bottom: int
    left: int
    right: int


class Blur(BaseModel):
    blur: int


class RGB(BaseModel):
    red: int
    green: int
    blue: int


class ImageProperties(BaseModel):
    name: str
    resize: Resize
    rotate: Rotate
    crop: Crop
    blur: Blur
    rgb: RGB


@image_tools_app.get("/", response_class=HTMLResponse)
async def image_tools(request: Request):
    return templates.TemplateResponse(request=request, name="image_tools.html")


@image_tools_app.post("/uploadfile/")
async def upload_file(file: UploadFile):
    file_path = os.path.join("media", file.filename)
    with open(file_path, "wb") as image:
        image.write(file.file.read())
    height, width = get_image_size(file_path)
    return {"filename": file.filename, "width": width, "height": height}


@image_tools_app.get("/image/", response_class=Response)
async def get_image(name: str = "no_image.png"):
    image_bytes = convert_image_to_bytes(f"media/{name}")
    return Response(
        content=image_bytes,
        media_type="image/jpeg",
        headers={"Cache-Control": "no-store"},
    )


@image_tools_app.post("/change/")
async def change_image(properties: ImageProperties):
    properties = properties.dict()

    name = properties.pop("name")
    file_path = f"media/{name}"
    changed_image = image_handler(file_path, **properties)
    image_bytes = convert_image_to_bytes(changed_image)

    new_name = f"new_{name}"
    new_file_path = f"media/{new_name}"
    with open(new_file_path, "wb") as image:
        image.write(image_bytes)

    return {"filename": new_name}


@image_tools_app.get("/save/", response_class=FileResponse)
async def save(name: str):
    file_path = os.path.join('media', name)
    return FileResponse(file_path, media_type='image/jpeg', filename=name)
