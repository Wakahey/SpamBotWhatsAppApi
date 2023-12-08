# Используем официальный образ Python 3.9
FROM python:3.10.12

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем все содержимое текущего каталога в /app внутри контейнера
COPY . /app

# Устанавливаем зависимости проекта
RUN pip install --no-cache-dir -r /app/requirements.txt

# Опционально: устанавливаем переменную среды PYTHONPATH
ENV PYTHONPATH=/app

# Открываем порт 8000
EXPOSE 8000

# Запускаем приложение
CMD ["uvicorn", "spambot.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]