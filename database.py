from sqlalchemy import create_engine, Column, Integer, LargeBinary, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Подключение к базе SQLite
DATABASE_URL = "sqlite:///./images.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Определение модели хранения изображений
class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)
    image_data = Column(LargeBinary, nullable=False)  # Храним как BLOB
    mime_type = Column(String, nullable=False)  # MIME-тип (jpeg, png и т. д.)

# Создаем таблицы
Base.metadata.create_all(bind=engine)