import cv2
import numpy as np
from scipy.ndimage import gaussian_filter


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
    if orig_image.image_data is None:
        print("There is no image")
        return
    print(f"______________{orig_image.image_data}")

    image_array = decode_db_to_cv(orig_image)
    (h, w) = image_array.shape[:2]
    center = (w // 2, h // 2)

    changed_images = []
    for i in range(1, count + 1):
        mtrx = cv2.getRotationMatrix2D(center, i*angle, 1.0)
        rotated = cv2.warpAffine(image_array, mtrx, (w, h))
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
            hsv[..., 1] = np.clip(hsv[..., 1] * np.random.uniform(0.5, 1.5), 0, 255)
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



def distortion_images(orig_image=None, options=""):
    """ Метод принимает оригинальное изображение из БД и создает список из
    искаженных изображений"""
    if orig_image is None:
        print("There is no image")
        return

    image_array = decode_db_to_cv(orig_image)

    changed_images = []
    if options == "distortion":
        # зеркальное отражение
        flipped_horizontally = cv2.flip(image_array, 1)
        changed_images.append(encode_cv_to_db(flipped_horizontally))

        # искажение перспективы
        height, width = image_array.shape[:2]
        max_x_offset = int(width * 0.2)
        max_y_offset = int(height * 0.2)
        orig_frame = np.float32([
                [0, 0],
                [width - 1, 0],
                [0, height - 1],
                [width - 1, height - 1]
                ])
        changed_frame = np.float32([
                [np.random.randint(0, max_x_offset), np.random.randint(0, max_y_offset)],
                [width - np.random.randint(0, max_x_offset), np.random.randint(0, max_y_offset)],
                [np.random.randint(0, max_x_offset), height - np.random.randint(0, max_y_offset)],
                [width - np.random.randint(0, max_x_offset), height - np.random.randint(0, max_y_offset)]
            ])
        matrix = cv2.getPerspectiveTransform(orig_frame, changed_frame)
        perspective_image = cv2.warpPerspective(image_array, matrix, (width, height))
        changed_images.append(encode_cv_to_db(perspective_image))

        # эластичное искажение
        shape = image_array.shape

        dx = gaussian_filter((np.random.rand(*shape[:2]) * 2 - 1), 5, mode="constant", cval=0) * 35
        dy = gaussian_filter((np.random.rand(*shape[:2]) * 2 - 1), 5, mode="constant", cval=0) * 35

        x, y = np.meshgrid(np.arange(shape[1]), np.arange(shape[0]))
        indices = (np.clip(y + dy, 0, shape[0] - 1).astype(np.float32),
                   np.clip(x + dx, 0, shape[1] - 1).astype(np.float32))

        distorted_image = cv2.remap(image_array, indices[1], indices[0], interpolation=cv2.INTER_LINEAR,
                                    borderMode=cv2.BORDER_REFLECT)
        changed_images.append(encode_cv_to_db(distorted_image))

    if options == "blur":
        # гауссово размытие
        gauss_blur = cv2.GaussianBlur(image_array, (5, 5), 0)
        changed_images.append(encode_cv_to_db(gauss_blur))
        # размытие по среднему значению
        average_blur = cv2.blur(image_array, (9, 9))
        changed_images.append(encode_cv_to_db(average_blur))
        # медианное размытие
        median_blur = cv2.medianBlur(image_array, 7)
        changed_images.append(encode_cv_to_db(median_blur))

    if options == "noise":
        # добавление шума соль и перец
        height, width = image_array.shape[:2]

        num_salt = int(0.02 * height * width)
        salt_coords = (np.random.randint(0, height, num_salt), np.random.randint(0, width, num_salt))

        num_pepper = int(0.02 * height * width)
        pepper_coords = (np.random.randint(0, height, num_pepper), np.random.randint(0, width, num_pepper))

        if len(image_array.shape) == 3:
            image_array[salt_coords[0], salt_coords[1], :] = 255
            image_array[pepper_coords[0], pepper_coords[1], :] = 0
        else:
            image_array[salt_coords] = 255
            image_array[pepper_coords] = 0
        changed_images.append(encode_cv_to_db(image_array))

        # гауссовый шум
        # поменьше
        gaussian_low = np.random.normal(20, 20, image_array.shape).astype(np.uint8)
        gauss_image_low = cv2.add(image_array, gaussian_low)
        changed_images.append(encode_cv_to_db(gauss_image_low))
        # побольше
        gaussian_high = np.random.normal(0, 10, image_array.shape).astype(np.uint8)
        gauss_image_high = cv2.add(image_array, gaussian_high)
        changed_images.append(encode_cv_to_db(gauss_image_high))

    return changed_images
