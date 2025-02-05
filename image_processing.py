import cv2

class ImageSingleton:
    _instance = None
    _image = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def set_image(self, image_path):
        """Загружает новое изображение, заменяя предыдущее."""
        self._image = cv2.imread(image_path)

    def get_image(self):
        """Возвращает текущее изображение."""
        return self._image

# # Проверка:
# img_manager1 = ImageSingleton()
# img_manager1.set_image("example.jpg")
#
# img_manager2 = ImageSingleton()
# print(img_manager1 is img_manager2)  # True (это один и тот же объект)
# print(img_manager2.get_image())  # Выведет объект изображения