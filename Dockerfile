FROM python:3.12.7

WORKDIR /app

COPY . .

RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN python -m pip install -r requirements.txt


CMD ["python", "main.py"]

