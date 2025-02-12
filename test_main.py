from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


# === Тест главной страницы ===
def test_home():
    response = client.get("/")
    assert response.status_code == 200


# === Тест загрузки изображения ===
def test_upload_image():
    with open("test/bus.jpg", "rb") as image_file:
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
    data = {"angle": 90, "count": 15}  # count > 100
    response = client.post("/do_rotate", data=data)

    assert response.status_code == 200


# === Тест валидации count (слишком большое значение) ===
def test_do_rotate_invalid_count():
    data = {"angle": 90, "count": 150}  # count > 100

    response = client.post("/do_rotate", data=data)

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
    data = {"options": ["brightness", "contrast"]}  # Пример настроек

    response = client.post("/do_color_correction", data=data)

    assert response.status_code == 200


# === Тест сохранения цветокоррекции ===
def test_save_color_correction():
    response = client.post("/save_color_correction")

    assert response.status_code == 200


# === Тест страницы искажения изображения ===
def test_distortion_page():
    response = client.get("/distortion")
    assert response.status_code == 200


# === Тест применения искажения ===
def test_do_distortion():
    data = {"options": "blur"}  # Пример настройки

    response = client.post("/do_distortion", data=data)

    assert response.status_code == 200


# === Тест сохранения искаженных изображений ===
def test_save_distortion():
    response = client.post("/save_distortion")

    assert response.status_code == 200
