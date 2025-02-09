from abc import ABC, abstractmethod
from database_models import ImageDB, ImageRotate, ImageColorCorrection, ImageDistortion
import base64
from image_proceccing_methods import rotate_images
import os



class ImageProcessing(ABC):
    """Базовый класс для всех типов обработки изображений"""
    @abstractmethod
    def generate_images(self, db,  options):
        pass
    @abstractmethod
    def get_images(self, db):
        pass
    @abstractmethod
    def save_images(self, db, save_dir):
        pass


class Rotate(ImageProcessing):
    """Класс поворота изображений"""

    def generate_images(self, db, options):
        """Считывает загруженное пользователем изображение, шаг угла поворота,
           количество изображений и на основе этих данных
           генерирует повернутые изображения и записывает их в БД """
        # удаляем предыдущее изображение
        db.query(ImageRotate).delete()
        # достаем загруженное пользователем изображение
        orig_image = db.query(ImageDB).first()
        if db.query(ImageDB).count() == 0:
            print(f"Таблица {ImageDB.__tablename__} данных пуста")
            return None
        # поворачиваем изображение
        changed_images = rotate_images(orig_image=orig_image, angle=options["angle"], count=options["count"])

        for i, img in enumerate(changed_images):
            # Добавляем новое изображение если в таблице images есть изображение
            file_name = orig_image.file_name + "_rotate_" + str((i+1)*options["angle"]) + "_degrees"
            new_image = ImageRotate(file_name = file_name , image_data=img, mime_type="image/jpeg")
            db.add(new_image)

        db.commit()

    def get_images(self, db):
        """Возвращает текущие изображения из БД"""
        image_entry = db.query(ImageRotate).all()

        if db.query(ImageRotate).count() == 0:
            print(f"Таблица {ImageRotate.__tablename__} данных пуста")
            return None

        images = []  # Список для хранения изображений
        for img in image_entry:
            encoded_image = base64.b64encode(img.image_data).decode("utf-8")
            images.append({
                "mime_type": img.mime_type,
                "encoded_image": encoded_image
            })
        return images

    def save_images(self, db, save_dir):
        """Сохранение повернутых изображений на жесткий диск пользователя"""
        image_entry = db.query(ImageRotate).all()

        if db.query(ImageRotate).count() == 0:
            print(f"Таблица {ImageRotate.__tablename__} данных пуста")
            return None

        for img in image_entry:
            image_data = img.image_data
            file_path = os.path.join(save_dir, img.file_name + ".jpg")

            with open(file_path, "wb") as image_file:
                image_file.write(image_data)



class ColorCorrection(ImageProcessing):
    """Класс цветокоррекции изображений"""

    def generate_images(self, db, options):
        """Считывает загруженное пользователем изображение, на основе него
           генерирует изображения c цветовой коррекцией и записывает их в БД """
        # Удаляем предыдущее изображение
        db.query(ImageColorCorrection).delete()
        image_entry = db.query(ImageDB).first()
        # Добавляем новое изображение если в таблице images есть изображение
        if image_entry:
            new_image = ImageColorCorrection(file_name = image_entry.file_name, image_data=image_entry.image_data, mime_type=image_entry.mime_type)
            db.add(new_image)
            db.commit()
            db.refresh(new_image)  # Обновляем объект, чтобы получить актуальные данные


    def get_images(self, db):
        """Возвращает текущие изображения из БД"""
        image_entry = db.query(ImageColorCorrection).all()

        if db.query(ImageColorCorrection).count() == 0:
            print(f"Таблица {ImageColorCorrection.__tablename__} данных пуста")
            return None

        images = []  # Список для хранения изображений
        for img in image_entry:
            encoded_image = base64.b64encode(img.image_data).decode("utf-8")
            images.append({
                "mime_type": img.mime_type,
                "encoded_image": encoded_image
            })
        return images

    def save_images(self, db, save_dir):
        pass



class Distortion(ImageProcessing):
    def generate_images(self, db, options):
        """Считывает загруженное пользователем изображение, на основе него
           генерирует искаженные изображения и записывает их в БД """
        # Удаляем предыдущее изображение
        db.query(ImageDistortion).delete()
        image_entry = db.query(ImageDB).first()
        # Добавляем новое изображение если в таблице images есть изображение
        if image_entry:
            new_image = ImageDistortion(file_name = image_entry.file_name, image_data=image_entry.image_data, mime_type=image_entry.mime_type)
            db.add(new_image)
            db.commit()
            db.refresh(new_image)  # Обновляем объект, чтобы получить актуальные данные

    def get_images(self, db):
        """Возвращает текущие изображения из БД"""
        image_entry = db.query(ImageDistortion).all()
        if db.query(ImageDistortion).count() == 0:
            print(f"Таблица {ImageDistortion.__tablename__} данных пуста")
            return None

        images = []  # Список для хранения изображений
        for img in image_entry:
            encoded_image = base64.b64encode(img.image_data).decode("utf-8")
            images.append({
                "mime_type": img.mime_type,
                "encoded_image": encoded_image
            })
        return images

    def save_images(self, db, save_dir):
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