from fastapi.responses import HTMLResponse
from fastapi import FastAPI, Request, File, UploadFile, Depends, Form
from fastapi.templating import Jinja2Templates

from pydantic import BaseModel
from typing import List, Generator

from sqlalchemy.orm import Session
from database.database import Database

from image_processing.image_singleton import ImageSingleton
from image_processing.image_processing_factory import ImageProcessingFactory
import os

# определяем абсолютный путь, где хранится main.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# определяем директорию хранения шаблонов JINJA
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
templates = Jinja2Templates(directory=TEMPLATES_DIR)

# создаем экземпляр базы данных
db_instance = Database()

# создаем FastAPI приложение
app = FastAPI(lifespan=db_instance.lifespan)


# Pydantic модели, для валидации передачи данных из форм в программу
class RotateOptions(BaseModel):
    angle: int
    count: int

    @classmethod
    def as_form(cls, angle: int = Form(...), count: int = Form(...)):
        return cls(angle=angle, count=count)


class ColorCorrectionOptions(BaseModel):
    options: List[str]

    @classmethod
    def as_form(cls, options: List[str] = Form(default=[])):
        return cls(options=options)


class DistortionOptions(BaseModel):
    options: str

    @classmethod
    def as_form(cls, options: str = Form(...)):
        return cls(options=options)


# задаем директорию для хранения аугментированных изображений
SAVE_DIR = os.path.join(BASE_DIR, "augmented_images")
os.makedirs(SAVE_DIR, exist_ok=True)

# создаем экземпляр класса изображения
img = ImageSingleton()

# создаем фабрику различных процессов обработки изображений
img_factory = ImageProcessingFactory()
rotate_process = img_factory.create_new_process("rotate")
color_correction_process = img_factory.create_new_process("color correction")
distortion_process = img_factory.create_new_process("distortion")

# глобальное хранение опций
ROTATE_OPTIONS = {}
COLOR_CORRECTION_OPTIONS = []
DISTORTION_OPTIONS = "distortion"

def get_db() -> Generator[Session, None, None]:
    """Создание и управление сессией БД"""
    db = db_instance.SessionLocal()
    try:
        yield db  # передаем сессию в обработчики запросов
    finally:
        db.close()  # закрываем соединение после выполнения запроса, чтобы избежать утечек памяти


# ===
# === Главная страница и загрузка оригинального изображения ===
# ===
@app.get("/", response_class=HTMLResponse)
async def home(request: Request, db: Session = Depends(get_db)):
    """Страница /"""
    return templates.TemplateResponse(request, "index.html", {
        "orig_image": img.get_image(db)
    })


@app.post("/")
async def upload_image(request: Request, db: Session = Depends(get_db),
                       file: UploadFile = File(..., description="Только изображения")):
    """Кнопка """
    if not file.content_type.startswith("image/"):
        return templates.TemplateResponse(request, "index.html", {
            "error": "Файл не является изображением",
            "orig_image": img.get_image(db)
        })
    image_data = await file.read()
    img.set_image_with_type(db, file.filename, image_data, file.content_type)

    return templates.TemplateResponse(request, "index.html", {
        "orig_image": img.get_image(db)
    })


# ===
# === Поворот изображения ===
# ===
@app.get("/rotate", response_class=HTMLResponse)
async def rotate(request: Request, db: Session = Depends(get_db)):
    global ROTATE_OPTIONS

    return templates.TemplateResponse(request, "rotate.html", {
        "rotate_options": ROTATE_OPTIONS,
        "rotate_images": rotate_process.get_images(db)
    })


@app.post("/do_rotate")
async def do_rotate(request: Request, db: Session = Depends(get_db),
                    options: RotateOptions = Depends(RotateOptions.as_form)):
    global ROTATE_OPTIONS
    ROTATE_OPTIONS = options.model_dump()
    if ROTATE_OPTIONS["count"] > 100:
        return templates.TemplateResponse(request, "rotate.html", {
            "rotate_options": ROTATE_OPTIONS,
            "error": "Вы пытаетесь сгенерировать слишком много изображений",
            "rotate_images": rotate_process.get_images(db)
        })
    if ROTATE_OPTIONS["count"] < 1:
        return templates.TemplateResponse(request, "rotate.html", {
            "rotate_options": ROTATE_OPTIONS,
            "error": "Вы пытаетесь повернуть изображение ничего раз и даже меньше",
            "rotate_images": rotate_process.get_images(db)
        })
    if ROTATE_OPTIONS["angle"] == 0:
        return templates.TemplateResponse(request, "rotate.html", {
            "rotate_options": ROTATE_OPTIONS,
            "error": "Вы пытаетесь сгенерировать копии картинок без поворота",
            "rotate_images": rotate_process.get_images(db)
        })

    rotate_process.generate_images(db, ROTATE_OPTIONS)

    return templates.TemplateResponse(request, "rotate.html", {
        "rotate_options": ROTATE_OPTIONS,
        "rotate_images": rotate_process.get_images(db)
    })


@app.post("/save_rotate")
async def save_rotate(request: Request, db: Session = Depends(get_db),
                      save_dir=SAVE_DIR):
    global ROTATE_OPTIONS
    rotate_process.save_images(db, save_dir)

    return templates.TemplateResponse(request, "rotate.html", {
        "rotate_options": ROTATE_OPTIONS,
        "rotate_images": rotate_process.get_images(db)
    })


# ===
# === Цветокоррекция изображения ===
# ===
@app.get("/color_correction", response_class=HTMLResponse)
async def color_correction(request: Request, db: Session = Depends(get_db)):
    global COLOR_CORRECTION_OPTIONS

    return templates.TemplateResponse(request, "color_correction.html", {
        "color_correction_options": COLOR_CORRECTION_OPTIONS,
        "color_correction_images": color_correction_process.get_images(db)
    })


@app.post("/do_color_correction")
async def do_color_correction(request: Request, db: Session = Depends(get_db),
                              options: ColorCorrectionOptions = Depends(ColorCorrectionOptions.as_form)):
    global COLOR_CORRECTION_OPTIONS
    COLOR_CORRECTION_OPTIONS = options.options

    color_correction_process.generate_images(db, COLOR_CORRECTION_OPTIONS)

    return templates.TemplateResponse(request, "color_correction.html", {
        "color_correction_options": COLOR_CORRECTION_OPTIONS,
        "color_correction_images": color_correction_process.get_images(db)
    })


@app.post("/save_color_correction")
async def save_color_correction(request: Request, db: Session = Depends(get_db),
                                save_dir=SAVE_DIR):
    global COLOR_CORRECTION_OPTIONS
    color_correction_process.save_images(db, save_dir)

    return templates.TemplateResponse(request, "color_correction.html", {
        "color_correction_options": COLOR_CORRECTION_OPTIONS,
        "color_correction_images": color_correction_process.get_images(db)
    })


# ===
# === Искажение изображения ===
# ===
@app.get("/distortion", response_class=HTMLResponse)
async def distortion(request: Request, db: Session = Depends(get_db)):
    global DISTORTION_OPTIONS

    return templates.TemplateResponse(request, "distortion.html", {
        "distortion_options": DISTORTION_OPTIONS,
        "distortion_images": distortion_process.get_images(db)
    })


@app.post("/do_distortion")
async def do_distortion(request: Request, db: Session = Depends(get_db),
                        options: DistortionOptions = Depends(DistortionOptions.as_form)):
    global DISTORTION_OPTIONS
    DISTORTION_OPTIONS = options.options
    distortion_process.generate_images(db, DISTORTION_OPTIONS)

    return templates.TemplateResponse(request, "distortion.html", {
        "distortion_options": DISTORTION_OPTIONS,
        "distortion_images": distortion_process.get_images(db)
    })


@app.post("/save_distortion")
async def save_distortion(request: Request, db: Session = Depends(get_db),
                          save_dir=SAVE_DIR):
    global DISTORTION_OPTIONS
    distortion_process.save_images(db, save_dir)

    return templates.TemplateResponse(request, "distortion.html", {
        "distortion_options": DISTORTION_OPTIONS,
        "distortion_images": distortion_process.get_images(db)
    })
