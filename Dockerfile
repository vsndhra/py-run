FROM python:3.10-alpine

RUN apk add --no-cache g++ openjdk11 nodejs php

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY templates/ templates/
COPY static/ static/

EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "1", "--threads", "8", "app:app"]

