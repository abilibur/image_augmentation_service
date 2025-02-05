import cv2
import base64

class ImageSingleton:
    __instance = None
    __image = None
    __image_type = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def set_image_with_type(self, image_data, file_type):
        """Загружает новое изображение, заменяя предыдущее."""
        self.__image = encoded_image = base64.b64encode(image_data).decode("utf-8")
        self.__image_type = file_type

    def get_image(self):
        """Возвращает текущее изображение."""
        return self.__image

    def get_image_type(self):
        """Возвращает текущее изображение."""
        return self.__image_type

