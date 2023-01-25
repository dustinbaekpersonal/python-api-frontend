# Dockerfile for flask app
# Build Context defined in docker-compose.yaml

FROM python:3.7
RUN python3 -m pip install --upgrade pip
RUN pip install gunicorn
RUN echo "alias list='ls -lastrh'" >> ~/.bashrc

RUN mkdir /dash

COPY . /dash

RUN python3 -m pip install -r /dash/requirements.txt

WORKDIR /dash

CMD python3 main.py # dev
