from fastapi.responses import HTMLResponse
from fastapi import FastAPI, Request, File, UploadFile, Depends, Form
from fastapi.templating import Jinja2Templates

from typing import List

from database import Database
from image_singleton import ImageSingleton
from image_processing_factory import ImageProcessingFactory
import os

# Определим директорию хранения шаблонов JINJA
templates = Jinja2Templates(directory="templates")

# Создаём экземпляр базы данных
db_instance = Database()

# Создаем FastAPI приложение
app = FastAPI(lifespan=db_instance.lifespan)

# Зададим директорию для сохранения аугментированных изображений
SAVE_DIR = "augmented_images"
os.makedirs(SAVE_DIR, exist_ok=True)

# Создаем экземпляр класса изображения
img = ImageSingleton()

# Создаем фабрику различных процессов обработки изображений
img_factory = ImageProcessingFactory()
rotate_process = img_factory.create_new_process("rotate")
ROTATE_OPTIONS = {}
color_correction_process = img_factory.create_new_process("color correction")
COLOR_CORRECTION_OPTIONS = []
distortion_process = img_factory.create_new_process("distortion")


def get_db():
    """Создаёт и управляет сессией БД"""
    db = db_instance.SessionLocal()
    try:
        yield db  # передаём сессию в обработчики запросов
    finally:
        db.close()  # закрываем соединение после выполнения запроса, чтобы избежать утечек памяти

# ---
# --- Главная страница и работа с оригинальным изображением ---
# ---
@app.get("/", response_class=HTMLResponse)
async def home(request: Request, db = Depends(get_db)):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "orig_image": img.get_image(db)
    })


@app.post("/")
async def upload_image(request: Request, file: UploadFile = File(...), db = Depends(get_db)):
    # Проверяем тип содержимого
    if not file.content_type.startswith("image/"):
        return templates.TemplateResponse("index.html", {
            "request": request,
            "error": "Файл не является изображением",
            "orig_image": img.get_image(db)
        })
    image_data = await file.read()
    img.set_image_with_type(db, file.filename, image_data, file.content_type)

    return templates.TemplateResponse("index.html", {
        "request": request,
        "orig_image": img.get_image(db)
    })


# ---
# --- Поворот изображения ---
# ---
@app.get("/rotate", response_class=HTMLResponse)
async def rotate(request: Request, db = Depends(get_db)):
    global ROTATE_OPTIONS
    return templates.TemplateResponse("rotate.html", {
        "request": request,
        "rotate_options": ROTATE_OPTIONS,
        "rotate_images": rotate_process.get_images(db)
    })

@app.post("/do_rotate")
async def do_rotate(request: Request, angle: int = Form(...),
                    count: int = Form(...), db = Depends(get_db)):
    global ROTATE_OPTIONS
    ROTATE_OPTIONS = {
        "angle": angle,
        "count": count
    }
    rotate_process.generate_images(db, ROTATE_OPTIONS)

    return templates.TemplateResponse("rotate.html", {
        "request": request,
        "rotate_options": ROTATE_OPTIONS,
        "rotate_images": rotate_process.get_images(db)
    })

@app.post("/save_rotate")
async def save_images(request: Request, db = Depends(get_db), save_dir=SAVE_DIR):
    global ROTATE_OPTIONS
    rotate_process.save_images(db, save_dir)

    return templates.TemplateResponse("rotate.html", {
        "request": request,
        "rotate_options": ROTATE_OPTIONS,
        "rotate_images": rotate_process.get_images(db)
    })


# ---
# --- Цветокоррекция изображения ---
# ---
@app.get("/color_correction", response_class=HTMLResponse)
async def color_correction(request: Request, db = Depends(get_db)):
    global COLOR_CORRECTION_OPTIONS
    return templates.TemplateResponse("color_correction.html", {
        "request": request,
        "color_correction_options": COLOR_CORRECTION_OPTIONS,
        "color_correction_images": color_correction_process.get_images(db)
    })


@app.post("/do_color_correction")
async def color_correction(request: Request, db = Depends(get_db),
                           options: List[str] = Form(default=[])):
    global COLOR_CORRECTION_OPTIONS
    COLOR_CORRECTION_OPTIONS = options

    color_correction_process.generate_images(db, COLOR_CORRECTION_OPTIONS)

    return templates.TemplateResponse("color_correction.html", {
        "request": request,
        "color_correction_options": COLOR_CORRECTION_OPTIONS,
        "color_correction_images": color_correction_process.get_images(db)
    })


@app.post("/save_color_correction")
async def save_images(request: Request, db = Depends(get_db),
                      save_dir=SAVE_DIR):
    color_correction_process.save_images(db, save_dir)
    global COLOR_CORRECTION_OPTIONS
    return templates.TemplateResponse("color_correction.html", {
        "request": request,
        "color_correction_options": COLOR_CORRECTION_OPTIONS,
        "color_correction_images": color_correction_process.get_images(db)
    })



# ---
# --- Искажение изображения ---
# ---
@app.get("/distortion", response_class=HTMLResponse)
async def distortion(request: Request, db = Depends(get_db)):
    # distortion_process.generate_images(db)
    return templates.TemplateResponse("distortion.html", {
        "request": request,
        "distortion_images": distortion_process.get_images(db)
    })
