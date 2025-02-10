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
            grayscale_image = cv2.cvtColor(image_array, cv2.COLOR_BGR2GRAY)
            changed_images.append(encode_cv_to_db(grayscale_image))
        if opt == "brightness":
            brightness_image = cv2.convertScaleAbs(image_array,alpha=1, beta=np.random.randint(-50, 50))
            changed_images.append(encode_cv_to_db(brightness_image))
        if opt == "contrast":
            contrast_image = cv2.convertScaleAbs(image_array, alpha=np.random.uniform(0.5, 1.5), beta=0)
            changed_images.append(encode_cv_to_db(contrast_image))
        if opt == "saturation":
            hsv = cv2.cvtColor(image_array, cv2.COLOR_BGR2HSV).astype(np.float32)
            # Умножаем S-канал на коэффициент и ограничиваем значения в диапазоне [0, 255]
            hsv[..., 1] = np.clip(hsv[..., 1] * np.random.uniform(0.5, 1.5), 0, 255)
            # Преобразуем обратно в BGR
            saturation_image = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)
            changed_images.append(encode_cv_to_db(saturation_image))
        if opt == "hue":
            hsv = cv2.cvtColor(image_array, cv2.COLOR_BGR2HSV).astype(np.int16)
            hsv[..., 0] = (hsv[..., 0] + np.random.randint(-20, 20)) % 180
            hsv_shift_image = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)
            changed_images.append(encode_cv_to_db(hsv_shift_image))
        if opt == "inversion":
            inverted_image = cv2.bitwise_not(image_array)
            changed_images.append(encode_cv_to_db(inverted_image))

    return changed_images





