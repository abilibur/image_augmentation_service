import sys
import os
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../database')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../image_processing')))

from fastapi.testclient import TestClient
from main import app, BASE_DIR
from database.database import Database


client = TestClient(app)

# === Добавляем
@pytest.fixture(scope='session', autouse=True)
def clear_database():
    db = Database()
    # Очистка базы перед тестами
    db.clear_database()
    yield  # выполняются тесты
    # Очистка базы после всех тестов
    db.clear_database()


# === Тест главной страницы ===
def test_home():
    response = client.get("/")
    assert response.status_code == 200


# === Тест загрузки изображения ===
def test_upload_image():
    TEST_JPG_DIR = os.path.join(BASE_DIR, "test/bus.jpg")
    with open(TEST_JPG_DIR, "rb") as image_file:
        image_content = image_file.read()
        files = {"file": ("bus.jpg", image_content, "image/png")}
        response = client.post("/", files=files)

        assert response.status_code == 200


# === Тест загрузки НЕ изображения ===
def test_upload_invalid_file():
    files = {"file": ("test.txt", b"Just a text file", "text/plain")}

    response = client.post("/", files=files)

    assert response.status_code == 200
    assert "Файл не является изображением" in response.text


# === Тест страницы поворота изображения ===
def test_rotate_page():
    response = client.get("/rotate")
    assert response.status_code == 200


# === Тест поворота изображения ===
def test_do_rotate():
    options = {"angle": 10, "count": 5}  # count > 100
    response = client.post("/do_rotate", data=options)

    assert response.status_code == 200


# === Тест валидации count (слишком большое значение) ===
def test_do_rotate_invalid_count():
    options = {"angle": 10, "count": 150}  # count > 100

    response = client.post("/do_rotate", data=options)

    assert response.status_code == 200
    assert "Вы пытаетесь сгенерировать слишком много изображений" in response.text


# === Тест сохранения повернутых изображений ===
def test_save_rotate():
    response = client.post("/save_rotate")

    assert response.status_code == 200


# === Тест страницы цветокоррекции ===
def test_color_correction_page():
    response = client.get("/color_correction")
    assert response.status_code == 200


# === Тест применения цветокоррекции ===
def test_do_color_correction():
    options = {"options": ["grayscale", "brightness", "contrast",
                           "saturation", "hue", "inversion"]}

    response = client.post("/do_color_correction", data=options)

    assert response.status_code == 200


# === Тест сохранения цветокоррекции ===
def test_save_color_correction():
    response = client.post("/save_color_correction")

    assert response.status_code == 200


# === Тест страницы искажения изображения ===
def test_distortion_page():
    response = client.get("/distortion")
    assert response.status_code == 200


# === Тест применения деформации ===
def test_do_distortion_distortion():
    data = {"options": "distortion"}  # Пример настройки

    response = client.post("/do_distortion", data=data)

    assert response.status_code == 200


# === Тест сохранения деформированных изображений ===
def test_save_distortion_distortion():
    response = client.post("/save_distortion")

    assert response.status_code == 200


# === Тест применения размытия ===
def test_do_distortion_blur():
    data = {"options": "blur"}  # Пример настройки

    response = client.post("/do_distortion", data=data)

    assert response.status_code == 200


# === Тест сохранения размытых изображений ===
def test_save_distortion_blur():
    response = client.post("/save_distortion")

    assert response.status_code == 200


# === Тест применения шума ===
def test_do_distortion_noise():
    data = {"options": "noise"}  # Пример настройки

    response = client.post("/do_distortion", data=data)

    assert response.status_code == 200


# === Тест сохранения зашумленных изображений ===
def test_save_distortion_noise():
    response = client.post("/save_distortion")

    assert response.status_code == 200
