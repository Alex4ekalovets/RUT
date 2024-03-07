import base64

from jinja2.filters import FILTERS

from fastapi import FastAPI, Request, Response, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse

from utils import image_handler, convert_image_to_bytes

app = FastAPI()

# FILTERS['b64encode'] = lambda x: base64.b64encode(x).decode("utf-8")

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def image_tools(request: Request):
    return templates.TemplateResponse(request=request, name="image_tools.html")

#
# @app.post("/uploadfile/")
# async def create_upload_file(file: UploadFile):
#     return {"filename": file.filename}


@app.get("/image", response_class=Response)
async def get_image():
    image = image_handler("test_data/2.jpg")
    image_bytes = convert_image_to_bytes(image)
    return Response(content=image_bytes, media_type="image/jpeg")


@app.post("/change")
async def change_image():
    pass


@app.get("/save_image", response_class=FileResponse)
async def save_image():
    pass
