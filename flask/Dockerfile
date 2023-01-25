# Dockerfile for flask app
# Build Context defined in docker-compose.yaml

FROM python:3.7
RUN python3 -m pip install --upgrade pip
RUN pip install gunicorn
RUN echo "alias list='ls -lastrh'" >> ~/.bashrc

RUN mkdir /flask

COPY . /flask

RUN python3 -m pip install -r /flask/requirements.txt

WORKDIR /flask
CMD python3 main.py # dev
#CMD gunicorn --bind=0.0.0.0:5000 --workers=4 main:app
