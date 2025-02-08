import cv2
import numpy as np
import base64

def rotate_images(orig_image=None, angle=1, count=4):
    if orig_image is None:
        print("There is no image")
        return

    # Декодируем бинарные данные изображения
    image_decode = np.frombuffer(orig_image.image_data, np.uint8)

    image_array = cv2.imdecode(image_decode, cv2.IMREAD_COLOR)
    # Получаем размеры изображения
    (h, w) = image_array.shape[:2]
    # Находим центр изображения
    center = (w // 2, h // 2)

    changed_images = []
    for i in range(1, count + 1):
        # Создаем матрицу поворота
        mtrx = cv2.getRotationMatrix2D(center, i*angle, 1.0)
        # Поворачиваем изображение
        rotated = cv2.warpAffine(image_array, mtrx, (w, h))

        # Кодируем повернутое изображение обратно в формат, который можно сохранить или отобразить
        _, buffer = cv2.imencode('.jpg', rotated)
        changed_images.append(buffer.tobytes())

    return changed_images




