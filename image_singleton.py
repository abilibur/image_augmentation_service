import base64
from database_models import ImageDB

class ImageSingleton:
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def set_image_with_type(self,db, image_data, file_type):
        """Загружает новое изображение, заменяя предыдущее в базе данных"""
        # Удаляем предыдущее изображение
        db.query(ImageDB).delete()

        # Добавляем новое изображение
        new_image = ImageDB(image_data=image_data, mime_type=file_type)
        db.add(new_image)
        db.commit()
        db.refresh(new_image)  # Обновляем объект, чтобы получить актуальные данные

    def get_image(self, db):
        """Возвращает текущее изображение из БД"""
        image_entry = db.query(ImageDB).first()
        if image_entry:
            return base64.b64encode(image_entry.image_data).decode("utf-8")
        return None

    def get_image_type(self, db):
        """Возвращает текущий тип изображения из БД"""
        image_entry = db.query(ImageDB).first()
        if image_entry:
            return image_entry.mime_type
        return None

