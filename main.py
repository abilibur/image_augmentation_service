from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from starlette.requests import Request


# Создаем FastAPI приложение
app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/image_rotate", response_class=HTMLResponse)
async def image_rotate(request: Request):
    return templates.TemplateResponse("image_rotate.html", {"request": request})

@app.get("/color_correction", response_class=HTMLResponse)
async def color_correction(request: Request):
    return templates.TemplateResponse("color_correction.html", {"request": request})

@app.get("/distortion", response_class=HTMLResponse)
async def distortion(request: Request):
    return templates.TemplateResponse("distortion.html", {"request": request})
