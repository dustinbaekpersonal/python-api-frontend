FROM python:3.12-slim

WORKDIR /dash

COPY . /dash

RUN pip install --upgrade pip
RUN pip install -r prod.txt

EXPOSE 8050