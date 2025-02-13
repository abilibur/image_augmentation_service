from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, LargeBinary, String

Base = declarative_base()


# Определение модели хранения изображений
# Модель ImageDB представляет собой таблицу с именем images
class ImageDB(Base):
    __tablename__ = "images"  # имя таблицы
    id = Column(Integer, primary_key=True, index=True)  # уникальный ID
    file_name = Column(String, nullable=False)  # имя загруженного файла
    image_data = Column(LargeBinary, nullable=False)  # хранение байтовых данных изображения
    mime_type = Column(String, nullable=False)  # тип изображения


# Определение модели хранения повернутых изображений
# Модель ImageRotate представляет собой таблицу с именем rotate_images
class ImageRotate(Base):
    __tablename__ = "rotate_images"  # имя таблицы
    file_name = Column(String, nullable=False)  # имя загруженного файла
    id = Column(Integer, primary_key=True, index=True)  # уникальный ID
    image_data = Column(LargeBinary, nullable=False)  # хранение байтовых данных изображения
    mime_type = Column(String, nullable=False)  # тип изображения


# Определение модели хранения изображений c цветовой коррекцией
# Модель ImageColorCorrection представляет собой таблицу с именем color_correction_images
class ImageColorCorrection(Base):
    __tablename__ = "color_correction_images"  # имя таблицы
    file_name = Column(String, nullable=False)  # имя загруженного файла
    id = Column(Integer, primary_key=True, index=True)  # уникальный ID
    image_data = Column(LargeBinary, nullable=False)  # хранение байтовых данных изображения
    mime_type = Column(String, nullable=False)  # тип изображения


# Определение модели хранения изображений с искажениями
# Модель ImageDistortion представляет собой таблицу с именем distortion_images
class ImageDistortion(Base):
    __tablename__ = "distortion_images"  # имя таблицы
    file_name = Column(String, nullable=False)  # имя загруженного файла
    id = Column(Integer, primary_key=True, index=True)  # уникальный ID
    image_data = Column(LargeBinary, nullable=False)  # хранение байтовых данных изображения
    mime_type = Column(String, nullable=False)  # тип изображения
