import cv2
import numpy as np


def decode_db_to_cv(db_image):
    """Декодируем бинарные данные изображения в массив numpy"""
    buffer = np.frombuffer(db_image.image_data, np.uint8)
    return cv2.imdecode(buffer, cv2.IMREAD_COLOR)


def encode_cv_to_db(array_image):
    """Кодируем изображение из массива numpy в формат который можно сохранить или отобразить"""
    _, buffer = cv2.imencode('.jpg', array_image)
    return buffer.tobytes()


def rotate_images(orig_image=None, angle=1, count=4):
    """ Метод принимает оригинальное изображение из БД и создает список из повернутых изображений"""
    if orig_image is None:
        print("There is no image")
        return

    image_array = decode_db_to_cv(orig_image)
    # получаем размеры изображения
    (h, w) = image_array.shape[:2]
    # находим центр изображения
    center = (w // 2, h // 2)

    changed_images = []
    for i in range(1, count + 1):
        # создаем матрицу поворота
        mtrx = cv2.getRotationMatrix2D(center, i*angle, 1.0)
        # поворачиваем изображение
        rotated = cv2.warpAffine(image_array, mtrx, (w, h))
        # добавляем в список кодированное изображение
        changed_images.append(encode_cv_to_db(rotated))

    return changed_images


def color_correction_images(orig_image=None, options=None):
    """ Метод принимает оригинальное изображение из БД и создает список из
    скорректированных по цвету изображений"""
    if orig_image is None:
        print("There is no image")
        return

    if options is None:
        options = []

    image_array = decode_db_to_cv(orig_image)

    changed_images = []
    for opt in options:
        if opt == "grayscale":
            gray_image = cv2.cvtColor(image_array, cv2.COLOR_BGR2GRAY)
            changed_images.append(encode_cv_to_db(gray_image))

    return changed_images





