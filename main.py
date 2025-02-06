from fastapi.responses import HTMLResponse
from fastapi import FastAPI, Request, File, UploadFile, Depends
from fastapi.templating import Jinja2Templates

from database import Database
from image_singleton import ImageSingleton
from image_processing_factory import ImageProcessingFactory

templates = Jinja2Templates(directory="templates")
# Создаём экземпляр базы данных
db_instance = Database()
# Создаем FastAPI приложение
app = FastAPI(lifespan=db_instance.lifespan)

# Создаем экземпляр класса изображения
img = ImageSingleton()
# Создаем фабрику различных процессов обработки изображений
img_factory = ImageProcessingFactory()
rotate_process = img_factory.create_new_process("rotate")
color_correction_process = img_factory.create_new_process("color correction")
distortion_process = img_factory.create_new_process("distortion")


def get_db():
    """Создаёт и управляет сессией БД"""
    db = db_instance.SessionLocal()
    try:
        yield db  # передаём сессию в обработчики запросов
    finally:
        db.close()  # закрываем соединение после выполнения запроса, чтобы избежать утечек памяти

@app.get("/", response_class=HTMLResponse)
async def home(request: Request, db = Depends(get_db)):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "encoded_image": img.get_image(db),
        "mime_type": img.get_image_type(db)
    })

@app.post("/")
async def upload_image(request: Request, file: UploadFile = File(...), db = Depends(get_db)):
    # Проверяем тип содержимого
    if not file.content_type.startswith("image/"):
        return templates.TemplateResponse("index.html", {
            "request": request,
            "error": "Файл не является изображением",
            "encoded_image": img.get_image(db),
            "mime_type": img.get_image_type(db)
        })
    # Читаем файл
    image_data = await file.read()
    # Загружаем данные файла в класс Singleton
    img.set_image_with_type(db, image_data, file.content_type)

    return templates.TemplateResponse("index.html", {
        "request": request,
        "encoded_image": img.get_image(db),
        "mime_type": img.get_image_type(db)
    })


@app.get("/rotate", response_class=HTMLResponse)
async def rotate(request: Request, db = Depends(get_db)):
    rotate_process.generate_images(db)
    images = [
        {"encoded_image": rotate_process.get_image(db),
        "mime_type": rotate_process.get_image_type(db)},
        {"encoded_image": rotate_process.get_image(db),
         "mime_type": rotate_process.get_image_type(db)},
        {"encoded_image": rotate_process.get_image(db),
         "mime_type": rotate_process.get_image_type(db)},
        {"encoded_image": rotate_process.get_image(db),
         "mime_type": rotate_process.get_image_type(db)},
        {"encoded_image": rotate_process.get_image(db),
         "mime_type": rotate_process.get_image_type(db)},
        {"encoded_image": rotate_process.get_image(db),
         "mime_type": rotate_process.get_image_type(db)},
        {"encoded_image": rotate_process.get_image(db),
         "mime_type": rotate_process.get_image_type(db)}
    ]
    return templates.TemplateResponse("rotate.html", {
        "request": request,
        "rotate_images": images
    })

@app.get("/color_correction", response_class=HTMLResponse)
async def color_correction(request: Request, db = Depends(get_db)):
    color_correction_process.generate_images(db)
    return templates.TemplateResponse("color_correction.html", {
        "request": request,
        "encoded_image": color_correction_process.get_image(db),
        "mime_type": color_correction_process.get_image_type(db)
    })

@app.get("/distortion", response_class=HTMLResponse)
async def distortion(request: Request, db = Depends(get_db)):
    distortion_process.generate_images(db)
    return templates.TemplateResponse("distortion.html", {
        "request": request,
        "encoded_image": distortion_process.get_image(db),
        "mime_type": distortion_process.get_image_type(db)
    })
