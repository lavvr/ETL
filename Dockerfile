FROM python:3.12.7-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app
RUN apt-get update && apt-get install -y gcc libpq-dev && rm -rf /var/lib/apt/lists/*
# Копируем файлы зависимостей
COPY requirements.txt requirements.txt
# Устанавливаем зависимости
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . .

# Указываем рабочую директорию (на всякий случай)
WORKDIR /app/lib

# Запускаем main.py
CMD ["python", "main.py"]

