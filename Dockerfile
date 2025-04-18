FROM python:3.13-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./api ./api
COPY ./templates ./templates/
COPY ./static ./static/

EXPOSE 5000

CMD ["gunicorn", "--chdir", "api", "app:app", "--bind", "0.0.0.0:5000", "--workers", "4", "--threads", "4"]
