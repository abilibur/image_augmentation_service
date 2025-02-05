from fastapi.responses import HTMLResponse
from fastapi import FastAPI, Request, File, UploadFile, Depends
from fastapi.templating import Jinja2Templates
import base64
from sqlalchemy.orm import Session
from database import SessionLocal, Image, lifespan


# Создаем FastAPI приложение
app = FastAPI(lifespan=lifespan)
templates = Jinja2Templates(directory="templates")


# Функция для получения сессии БД
async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/", response_class=HTMLResponse)
async def home(request: Request, db: Session = Depends(get_db)):
    # Получаем последнее загруженное изображение
    first_image = db.query(Image).order_by(Image.id.asc()).first()

    if first_image:
        encoded_image = base64.b64encode(first_image.image_data).decode("utf-8")
        mime_type = first_image.mime_type
    else:
        encoded_image = None
        mime_type = None

    return templates.TemplateResponse("index.html", {
        "request": request,
        "encoded_image": encoded_image,
        "mime_type": mime_type
    })

@app.post("/")
async def upload_image(request: Request, file: UploadFile = File(...), db: Session = Depends(get_db)):

    # Проверка типа содержимого
    if not file.content_type.startswith("image/"):
        first_image = db.query(Image).order_by(Image.id.asc()).first()
        encoded_image = base64.b64encode(first_image.image_data).decode("utf-8") if first_image else None
        mime_type = first_image.mime_type if first_image else None

        return templates.TemplateResponse("index.html", {
            "request": request,
            "error": "Файл не является изображением",
            "encoded_image": encoded_image,
            "mime_type": mime_type
        })
    # Читаем файл
    image_data = await file.read()

    # Сохраняем в БД
    new_image = Image(image_data=image_data, mime_type=file.content_type)
    db.add(new_image)
    db.commit()

    return await home(request, db)  # Перенаправляем на главную



@app.get("/image_rotate", response_class=HTMLResponse)
async def image_rotate(request: Request):
    return templates.TemplateResponse("image_rotate.html", {"request": request})

@app.get("/color_correction", response_class=HTMLResponse)
async def color_correction(request: Request):
    return templates.TemplateResponse("color_correction.html", {"request": request})

@app.get("/distortion", response_class=HTMLResponse)
async def distortion(request: Request):
    return templates.TemplateResponse("distortion.html", {"request": request})
