FROM python:3.12-slim

WORKDIR /app
COPY req.txt .

RUN pip install --user --no-cache-dir -r req.txt
