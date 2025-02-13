# Сервис аугментации изображений

Веб-сервис для создания различных деформированных изображений.\
\
![Python](https://img.shields.io/badge/-Python-3776AB?style=flat&logo=python&logoColor=white)
![HTML](https://img.shields.io/badge/-HTML-E34F26?style=flat&logo=html5&logoColor=white)
---

### Описание

Аугментация изображений позволяет частично решить проблему нехватки данных для машинного обучения или обучения нейронных
сетей.

Данный сервис позволяет пользователю создавать пакет различных деформированных изображений на основе изображения
выбранного пользователем.
Так же, перед сохранением на жесткий диск изображения визуализируются для валидации деформаций пользователем.

---

### Установка

#### 1. Клонируйте репозиторий

```
git clone https://github.com/abilibur/image_augmentation_service
```

#### 2. Перейдите в директорию image_augmentation_service

```
cd image_augmentation_service
```

#### 3. Создайте и активируйте виртуальное окружение:

Linux/Mac:

```
python3 -m venv venv
source venv/bin/activate 
```

Windows:

```
python3 -m venv venv
venv\Scripts\activate.bat
```

#### 4. Установите зависимости

```
pip install -r requirements.txt
```

### Запуск

#### 5. Запуск сервера uvicorn

В папке с проектом выполнить:

```
uvicorn main:app --reload
```

#### 6. Переход на главную веб страницу

Введите в строке браузера (или кликните по ссылке):

[`http://127.0.0.1:8000`](http://127.0.0.1:8000)

#### 7. Для лучшего понимания работы в приложении ознакомьтесь с руководством пользователя 
[User Guide](UserGuide.md)

---

### Запуск тестирования pytest

В папке с проектом выполнить:

```
pytest
```

Знак успешного выполнения тестов:

```
test\test_main.py .................                           [100%]

======================== 17 passed in 2.69s ========================
```

---

## Структура проекта

```
image_augmentation_service
│
├── augmented_images                    # Папка, куда сохраняются деформированные изображения. Директория создается после запуска приложения
├── database                            # Модуль управления работой базы данных c изображениями  
│    ├── __init__.py
│    ├── database.py                    
│    ├── database_models.py             
│    └── images.db                      # База данных SQLite, создается после начала работы с приложением
├── image_processing                    # Модуль отвечающий за обработку изображений, а так же за получение и запись изображений в базу данных      
│    ├── __init__.py
│    ├── image_processing_factory.py    
│    ├── image_processing_methods.py                
│    └── image_singleton.py
├── templates                           # Шаблоны Jinja
│    ├── color_correction.html
│    ├── distortion.html
│    ├── index.html              
│    └── rotate.html
├── test                                # Модуль содержащий тесты для приложения  
│    ├── images_for_manual_testing      # Папка содержащая примеры изображений для загрузкки в приложение
│    ├── __init__.py
│    ├── bus.jpg
│    └── test_main.py
├── __init__.py
├── main.py
├── requirements.txt
├── UserGuide.md                        # Руководство пользователя
└── README.md                           # Документация
```
