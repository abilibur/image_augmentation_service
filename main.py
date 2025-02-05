from fastapi.responses import HTMLResponse
from fastapi import FastAPI, Request, File, UploadFile
from fastapi.templating import Jinja2Templates
from image_processing import ImageSingleton


# Создаем FastAPI приложение
app = FastAPI()
templates = Jinja2Templates(directory="templates")
img = ImageSingleton()


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "encoded_image": img.get_image(),
        "mime_type": img.get_image_type()
    })

@app.post("/")
async def upload_image(request: Request, file: UploadFile = File(...)):

    # Проверка типа содержимого
    if not file.content_type.startswith("image/"):
        return templates.TemplateResponse("index.html", {
            "request": request,
            "error": "Файл не является изображением",
            "encoded_image": img.get_image(),
            "mime_type": img.get_image_type()
        })

    # Читаем файл
    image_data = await file.read()

    # загружаем данные файла в класс Singleton
    img.set_image_with_type(image_data, file.content_type)

    return templates.TemplateResponse("index.html", {
        "request": request,
        "encoded_image": img.get_image(),
        "mime_type": img.get_image_type()
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
