from abc import ABC, abstractmethod
from database_models import ImageDB, ImageRotate, ImageColorCorrection, ImageDistortion
import base64

# Базовый класс для всех типов обработки изображений
class ImageProcessing(ABC):
    @abstractmethod
    def generate_images(self, db):
        pass
    @abstractmethod
    def get_image(self, db):
        pass
    @abstractmethod
    def get_image_type(self, db):
        pass

class Rotate(ImageProcessing):
    def generate_images(self, db):
        """ """
        # Удаляем предыдущее изображение
        db.query(ImageRotate).delete()
        image_entry = db.query(ImageDB).first()
        # Добавляем новое изображение если в таблице images есть изображение
        if image_entry:
            new_image = ImageRotate(image_data=image_entry.image_data, mime_type=image_entry.mime_type)
            db.add(new_image)
            db.commit()
            db.refresh(new_image)  # Обновляем объект, чтобы получить актуальные данные

    def get_image(self, db):
        """Возвращает текущее изображение из БД"""
        image_entry = db.query(ImageRotate).first()
        if image_entry:
            return base64.b64encode(image_entry.image_data).decode("utf-8")
        return None

    def get_image_type(self, db):
        """Возвращает текущий тип изображения из БД"""
        image_entry = db.query(ImageRotate).first()
        if image_entry:
            return image_entry.mime_type
        return None


class ColorCorrection(ImageProcessing):
    def generate_images(self, db):
        return "color"
    def get_image(self, db):
        pass
    def get_image_type(self, db):
        pass

# Конкретные классы
class Distortion(ImageProcessing):
    def generate_images(self, db):
        return "distortion"
    def get_image(self, db):
        pass
    def get_image_type(self, db):
        pass

# Фабрика
class ImageProcessingFactory:
    @staticmethod
    def create_new_process(processing_type: str) -> ImageProcessing:
        if processing_type == "rotate":
            return Rotate()
        elif processing_type == "color correction":
            return ColorCorrection()
        elif processing_type == "distortion":
            return Distortion()
        else:
            raise ValueError("Неподдерживаемый тип обработки изображения")