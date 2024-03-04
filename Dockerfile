FROM python:3.12-slim

WORKDIR /app

COPY asdf.py /app
# COPY requirements/ /app

RUN pip install fastapi uvicorn

