from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from apps.image_tools_app import image_tools_app
from apps.detection import detection_app
import settings

app = FastAPI()
app.mount("/image_tools", image_tools_app)
app.mount("/detection", detection_app)

image_tools_app = FastAPI(title="Image Tools")
detection_app = FastAPI(title="Detection")

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")
