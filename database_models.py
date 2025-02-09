from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, LargeBinary, String

Base = declarative_base()

# Определение модели хранения изображений
# Модель ImageDB представляет собой таблицу с именем images
class ImageDB(Base):
    __tablename__ = "images"  # имя таблицы
    id = Column(Integer, primary_key=True, index=True)  # Уникальный ID
    file_name = Column(String, nullable=False) # имя загруженного файла
    image_data = Column(LargeBinary, nullable=False)  # Хранит байтовые данные изображения (тип BLOB в SQLite))
    mime_type = Column(String, nullable=False)  # MIME-тип - тип изображения (jpeg, png и т. д.)

# Определение модели хранения повернутых изображений
# Модель ImageDB представляет собой таблицу с именем images
class ImageRotate(Base):
    __tablename__ = "rotate_images"  # имя таблицы
    file_name = Column(String, nullable=False)  # имя загруженного файла
    id = Column(Integer, primary_key=True, index=True)  # Уникальный ID
    image_data = Column(LargeBinary, nullable=False)  # Хранит байтовые данные изображения (тип BLOB в SQLite))
    mime_type = Column(String, nullable=False)  # MIME-тип - тип изображения (jpeg, png и т. д.)

# Определение модели хранения изображений c цветовой коррекцией
# Модель ImageDB представляет собой таблицу с именем images
class ImageColorCorrection(Base):
    __tablename__ = "color_correction_images"  # имя таблицы
    file_name = Column(String, nullable=False)  # имя загруженного файла
    id = Column(Integer, primary_key=True, index=True)  # Уникальный ID
    image_data = Column(LargeBinary, nullable=False)  # Хранит байтовые данные изображения (тип BLOB в SQLite))
    mime_type = Column(String, nullable=False)  # MIME-тип - тип изображения (jpeg, png и т. д.)

# Определение модели хранения повернутых изображений с искажениями
# Модель ImageDB представляет собой таблицу с именем images
class ImageDistortion(Base):
    __tablename__ = "distortion_images"  # имя таблицы
    file_name = Column(String, nullable=False)  # имя загруженного файла
    id = Column(Integer, primary_key=True, index=True)  # Уникальный ID
    image_data = Column(LargeBinary, nullable=False)  # Хранит байтовые данные изображения (тип BLOB в SQLite))
    mime_type = Column(String, nullable=False)  # MIME-тип - тип изображения (jpeg, png и т. д.)