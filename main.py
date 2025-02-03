from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from starlette.requests import Request
from fastapi import FastAPI, Request, File, UploadFile
import base64

# Создаем FastAPI приложение
app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/")
async def upload_image(request: Request, file: UploadFile = File(...)):
    # Проверка типа содержимого
    if not file.content_type.startswith("image/"):
        return templates.TemplateResponse("index.html", {
            "request": request,
            "error": "Файл не является изображением"
        })

    # Чтение и кодирование изображения
    image_data = await file.read()
    encoded_image = base64.b64encode(image_data).decode("utf-8")

    return templates.TemplateResponse("index.html", {
        "request": request,
        "mime_type": file.content_type,
        "encoded_image": encoded_image
    })

@app.get("/image_rotate", response_class=HTMLResponse)
async def image_rotate(request: Request):
    return templates.TemplateResponse("image_rotate.html", {"request": request})

@app.get("/color_correction", response_class=HTMLResponse)
async def color_correction(request: Request):
    return templates.TemplateResponse("color_correction.html", {"request": request})

@app.get("/distortion", response_class=HTMLResponse)
async def distortion(request: Request):
    return templates.TemplateResponse("distortion.html", {"request": request})
