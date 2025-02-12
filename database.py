from fastapi import FastAPI
from sqlalchemy import create_engine, text

from sqlalchemy.orm import sessionmaker
from contextlib import asynccontextmanager
from database_models import Base

class Database:
    """Класс для управления базой данных и сессиями."""
    def __init__(self):
        # Подключаемся к базе SQLite
        # check_same_thread=False — позволяет использовать одно соединение с базой
        #                           в разных потоках (нужно для FastAPI)
        self.DATABASE_URL = "sqlite:///./images.db"
        self.engine = create_engine(self.DATABASE_URL, connect_args={"check_same_thread": False}, echo=True)

        # Создаём сессии для работы с БД
        # autocommit=False — изменения в БД требуют commit().
        # autoflush=False — не сбрасывает данные автоматически, только при commit().
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

        # Создаём таблицы, если их ещё нет
        self.create_tables()


    def create_tables(self):
        """ Создает таблицы в базе данных, если их ещё нет """
        Base.metadata.create_all(bind=self.engine)


    def clear_database(self):
        """Очищает таблицу перед завершением работы сервера."""
        with self.engine.connect() as conn:

            conn.execute(text("DELETE FROM images"))  # Удаляем все записи images
            conn.execute(text("DELETE FROM rotate_images"))  # Удаляем все записи rotate_images
            conn.execute(text("DELETE FROM color_correction_images"))  # Удаляем все записи color_correction_images
            conn.execute(text("DELETE FROM distortion_images"))  # Удаляем все записи distortion_images
            conn.commit()
            # Освобождаем неиспользуемое пространство
            conn.execute(text("VACUUM"))  # Уменьшаем размер файла БД
            conn.commit()

    @asynccontextmanager
    async def lifespan(self):
        """ Асинхронный менеджер контекста для выполнения кода до и после работы сервера."""
        yield
        print("Очищаем базу перед остановкой сервера...")
        self.clear_database()