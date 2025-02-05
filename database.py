from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Integer, LargeBinary, String, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from contextlib import asynccontextmanager

# Подключаемся к базе SQLite
DATABASE_URL = "sqlite:///./images.db"
# check_same_thread=False — позволяет использовать соединение с базой
#                           в разных потоках (нужно для FastAPI)
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Создаём фабрику сессий для взаимодействия с базой данных
# autocommit=False — изменения в БД требуют commit().
# autoflush=False — не сбрасывает данные автоматически, только при commit().
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# базовый класс Base, от которого будут наследоваться все модели базы данных
Base = declarative_base()

# Определение модели хранения изображений
class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True) # Уникальный ID
    image_data = Column(LargeBinary, nullable=False)  # Данные изображения (BLOB)
    mime_type = Column(String, nullable=False)  # MIME-тип - тип изображения (jpeg, png и т. д.)


# Создаем таблицы в базе данных, если их ещё нет
Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app:FastAPI):
    yield # Сервер работает до этого момента
    print("Очистка базы данных перед остановкой сервера...")
    with engine.connect() as conn:
        conn.execute(text("DELETE FROM images"))  # Удаляем все записи
        conn.commit()

        # Освобождаем неиспользуемое пространство
        conn.execute(text("VACUUM"))  # Уменьшаем размер файла БД
        conn.commit()