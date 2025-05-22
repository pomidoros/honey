# Используем официальный образ Python
FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /code

# Копируем файлы проекта
COPY requirements.txt .
COPY ./main.py /code
COPY ./app /code/app

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

CMD python main.py
