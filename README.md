# Социальная сеть (Backend)

## Запуск проекта

1. Перейти в каталог проекта:
```bash
cd spd-diplom/social_network
```

2. Создать виртуальное окружение:
```bash
python -m venv .venv
source .venv/Scripts/activate
```

3. Установить зависимости:
```bash
pip install -r requirements.txt
```

4. Создать файл .env рядом с manage.py:
```
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
POSTGRES_DB=dj_diplom
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

5. Выполнить миграции:
```bash
python manage.py migrate
```

6. Создать суперпользователя:
```bash
python manage.py createsuperuser
```

7. Запустить сервер:
```bash
python manage.py runserver
```

Готово! API доступно на http://127.0.0.1:8000/api/
