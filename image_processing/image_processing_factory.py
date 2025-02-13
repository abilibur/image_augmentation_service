import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../image_processing')))

from abc import ABC, abstractmethod
from database.database_models import ImageDB, ImageRotate, ImageColorCorrection, ImageDistortion
import base64
from image_processing_methods import rotate_images, color_correction_images, distortion_images
import os


class ImageProcessing(ABC):
    """Базовый класс для всех типов обработки изображений"""

    @abstractmethod
    def generate_images(self, db, options):
        pass

    @abstractmethod
    def get_images(self, db):
        pass

    @abstractmethod
    def save_images(self, db, save_dir):
        pass


class Rotate(ImageProcessing):
    """Класс поворота изображения"""

    def generate_images(self, db, options):
        """Получение загруженного пользователем оригинального изображения,
           шага угла поворота и количества изображений. На основе этих данных
           генерация повернутых изображений и запись их в базу данных"""
        # очищаем таблицу с повернутыми изображениями перед генерацией новых
        db.query(ImageRotate).delete()

        # достаем загруженное пользователем оригинальное изображение
        orig_image = db.query(ImageDB).first()

        if db.query(ImageDB).count() == 0:
            print(f"Таблица {ImageDB.__tablename__} данных пуста")
            return None

        # поворачиваем изображение
        changed_images = rotate_images(orig_image=orig_image, angle=options["angle"], count=options["count"])

        # добавляем повернутые изображения в таблицу
        for i, img in enumerate(changed_images):
            file_name = orig_image.file_name + "_rotate_" + str((i + 1) * options["angle"]) + "_degrees"
            new_image = ImageRotate(file_name=file_name, image_data=img, mime_type="image/jpeg")
            db.add(new_image)

        db.commit()

    def get_images(self, db):
        """Получение текущих изображений из таблицы с повернутыми изображениями"""
        # получаем все изображения из таблицы
        image_entry = db.query(ImageRotate).all()

        if db.query(ImageRotate).count() == 0:
            print(f"Таблица {ImageRotate.__tablename__} данных пуста")
            return None

        images = []
        for img in image_entry:
            encoded_image = base64.b64encode(img.image_data).decode("utf-8")
            images.append({
                "mime_type": img.mime_type,
                "encoded_image": encoded_image
            })
        return images

    def save_images(self, db, save_dir):
        """Сохранение повернутых изображений на жесткий диск пользователя"""
        # получаем все изображения из таблицы
        image_entry = db.query(ImageRotate).all()

        if db.query(ImageRotate).count() == 0:
            print(f"Таблица {ImageRotate.__tablename__} данных пуста")
            return None

        # сохраняем в файл
        for img in image_entry:
            image_data = img.image_data
            file_path = os.path.join(save_dir, img.file_name + ".jpg")

            with open(file_path, "wb") as image_file:
                image_file.write(image_data)


class ColorCorrection(ImageProcessing):
    """Класс цветокоррекции изображений"""

    def generate_images(self, db, options):
        """Получение загруженного пользователем оригинального изображения и
           опций цветокоррекции из нажатых чекбоксов. На основе этих данных
           генерация изображений c цветовой коррекцией и запись их в базу данных"""
        # очищаем таблицу изображений с цветокоррекцией перед генерацией новых
        db.query(ImageColorCorrection).delete()

        # достаем загруженное пользователем оригинальное изображение
        orig_image = db.query(ImageDB).first()
        if db.query(ImageDB).count() == 0:
            print(f"Таблица {ImageDB.__tablename__} данных пуста")
            return None

        # цветокоррекция изображения
        changed_images = color_correction_images(orig_image=orig_image, options=options)

        # добавляем изображения с цветокоррекцией в таблицу
        for opt, img in zip(options, changed_images):
            file_name = orig_image.file_name + "_color_correction_" + opt
            new_image = ImageColorCorrection(file_name=file_name, image_data=img, mime_type="image/jpeg")
            db.add(new_image)

        db.commit()

    def get_images(self, db):
        """Получение текущих изображений из таблицы изображений с цветокоррекцией"""
        # получаем все изображения из таблицы
        image_entry = db.query(ImageColorCorrection).all()

        if db.query(ImageColorCorrection).count() == 0:
            print(f"Таблица {ImageColorCorrection.__tablename__} данных пуста")
            return None

        images = []
        for img in image_entry:
            encoded_image = base64.b64encode(img.image_data).decode("utf-8")
            images.append({
                "mime_type": img.mime_type,
                "encoded_image": encoded_image
            })
        return images

    def save_images(self, db, save_dir):
        """Сохранение изображений с цветокоррекцией на жесткий диск пользователя"""

        # получаем все изображения из таблицы
        image_entry = db.query(ImageColorCorrection).all()

        if db.query(ImageColorCorrection).count() == 0:
            print(f"Таблица {ImageColorCorrection.__tablename__} данных пуста")
            return None

        # сохраняем в файл
        for img in image_entry:
            image_data = img.image_data
            file_path = os.path.join(save_dir, img.file_name + ".jpg")

            with open(file_path, "wb") as image_file:
                image_file.write(image_data)


class Distortion(ImageProcessing):
    """Класс искажения изображений"""

    def generate_images(self, db, options):
        """Получение загруженного пользователем оригинального изображения и
           типа искажения выбранного в выпадающем меню. На основе этих данных
           генерация изображений c искажениями и запись их в базу данных"""
        # очищаем таблицу изображений с искажениями перед генерацией новых
        db.query(ImageDistortion).delete()

        # достаем загруженное пользователем оригинальное изображение
        orig_image = db.query(ImageDB).first()
        if db.query(ImageDB).count() == 0:
            print(f"Таблица {ImageDB.__tablename__} данных пуста")
            return None

        # искажение изображения
        changed_images = distortion_images(orig_image=orig_image, options=options)

        # добавляем изображения с искажениями в таблицу
        for i, img in enumerate(changed_images):
            file_name = orig_image.file_name + "_" + options + "_" + str(i + 1)
            new_image = ImageDistortion(file_name=file_name, image_data=img, mime_type="image/jpeg")
            db.add(new_image)

        db.commit()

    def get_images(self, db):
        """Получение текущих изображений из таблицы изображений с искажениями"""
        # получаем все изображения из таблицы
        image_entry = db.query(ImageDistortion).all()
        if db.query(ImageDistortion).count() == 0:
            print(f"Таблица {ImageDistortion.__tablename__} данных пуста")
            return None

        images = []
        for img in image_entry:
            encoded_image = base64.b64encode(img.image_data).decode("utf-8")
            images.append({
                "mime_type": img.mime_type,
                "encoded_image": encoded_image
            })
        return images

    def save_images(self, db, save_dir):
        """Сохранение изображений после искажения на жесткий диск пользователя"""
        # получаем все изображения из таблицы
        image_entry = db.query(ImageDistortion).all()

        if db.query(ImageDistortion).count() == 0:
            print(f"Таблица {ImageDistortion.__tablename__} данных пуста")
            return None

        # сохраняем в файл
        for img in image_entry:
            image_data = img.image_data
            file_path = os.path.join(save_dir, img.file_name + ".jpg")

            with open(file_path, "wb") as image_file:
                image_file.write(image_data)


# Фабрика обработки оригинального изображения
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
