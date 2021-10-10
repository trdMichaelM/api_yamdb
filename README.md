### Описание проекта:
Учебный проект, предназначенный для отработки навыков и применение теории при командной
разработки API для веб приложения YaMDb, базируемых на фреймворке Django и модуле Django Rest Framework.
Для обеспечения контороля прав доступа в проекте используется модуль JWT-токен.

### Установка и запуск проекта:

Клонировать репозиторий и перейти в него в командной строке (испольщуем ssh):

```
git clone git@github.com:trdMichaelM/api_yamdb.git
```

```
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

```
source venv/bin/activate (for Linux)
```

Обновить pip до последней версии:
```
python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Дополнительно установить модули Simple JWT:

```
pip install djangorestframework_simplejwt 
```

Выполнить миграции:

```
python3 manage.py makemigrations
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```

### Примеры использования API:

```
Дитальное описание и примеры работы API проекта представлены в 
документации: http://127.0.0.1:8000/redoc/ в формате ReDoc.
