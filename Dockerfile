# Dockerfile

# Використовуємо офіційний образ Python
FROM python:3.11

# Встановлюємо залежності системи
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev

# Встановлюємо робочий каталог
WORKDIR /app

# Копіюємо залежності (файли requirements.txt)
COPY requirements.txt /app/requirements.txt

# Встановлюємо всі залежності
RUN pip install --no-cache-dir -r /app/requirements.txt

# Копіюємо решту файлів проекту
COPY . /app

# Встановлюємо середовище для Django
ENV DJANGO_SETTINGS_MODULE=event_manager.settings
RUN python manage.py collectstatic --noinput
RUN python manage.py migrate

# Команда для запуску Celery
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
