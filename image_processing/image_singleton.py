import base64
from database.database_models import ImageDB, ImageRotate, ImageColorCorrection, ImageDistortion


class ImageSingleton:
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def set_image_with_type(self,db, file_name, image_data, mime_type):
        """Загружает новое изображение, заменяя предыдущее в базе данных"""
        # Удаляем предыдущее изображение
        db.query(ImageDB).delete()
        db.query(ImageRotate).delete()
        db.query(ImageColorCorrection).delete()
        db.query(ImageDistortion).delete()
        # удаляем расширение
        file_name = file_name.rsplit('.', 1)[0]
        # Добавляем новое изображение
        new_image = ImageDB(file_name=file_name,image_data=image_data, mime_type=mime_type)
        db.add(new_image)
        db.commit()
        db.refresh(new_image)  # Обновляем объект, чтобы получить актуальные данные

    def get_image(self, db):
        """Возвращает текущее изображение и тип изображения из БД"""
        image_entry = db.query(ImageDB).first()
        if image_entry:
            return {
                "mime_type": image_entry.mime_type,
                "encoded_image": base64.b64encode(image_entry.image_data).decode("utf-8")
            }
        return None
