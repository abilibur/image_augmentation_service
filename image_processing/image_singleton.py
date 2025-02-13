import base64
from database.database_models import ImageDB, ImageRotate, ImageColorCorrection, ImageDistortion


class ImageSingleton:
    """Класс сохранения в базу данных и получения из базы данных оригинального изображения"""
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def set_image(self, db, file_name, image_data, mime_type):
        """Загрузка нового изображения, очистив все таблицы в базе данных."""
        # очищаем таблицы в базе данных
        db.query(ImageDB).delete()
        db.query(ImageRotate).delete()
        db.query(ImageColorCorrection).delete()
        db.query(ImageDistortion).delete()

        # удаляем расширение у имени файла
        file_name = file_name.rsplit('.', 1)[0]

        # добавляем новое изображение в таблицу с оригинальных изображением
        new_image = ImageDB(file_name=file_name, image_data=image_data, mime_type=mime_type)
        db.add(new_image)
        db.commit()
        db.refresh(new_image)  # обновляем объект, чтобы получить актуальные данные

    def get_image(self, db):
        """Получение текущего оригинального изображения и типа изображения из базы данных"""
        # получаем первый и единственный элемент из таблицы оригинального изображения
        image_entry = db.query(ImageDB).first()
        if image_entry:
            return {
                "mime_type": image_entry.mime_type,
                "encoded_image": base64.b64encode(image_entry.image_data).decode("utf-8")
            }
        return None
