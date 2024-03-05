# API and Frontend

This repository illustrates how to develop APIs and how web applications interact with APIs to retrieve data that user asked for.

For API backend service, we use FastAPI.
For frontend, we use Dash.
For database, we use PostgreSQL.


## :wrench: Developer set up

First clone the repo. In a terminal, navigate to a folder you want to clone the code to then run:

1. Clone the repo
```bash
$ git clone git@github.com:dustinbaekpersonal/python-api-frontend.git
```

2. Create virtual environment and activate
```bash
make uv-setup && source .venv/bin/activate
```

3. Install dependencies
```bash
make uv-dev
```

4. To run pre-commit,
```bash
pre-commit install
```

## :steam_locomotive: Running Docker container

To emulate realistic environment, we will use docker containers for database and web server.

Pre-requisite:
You need to install docker on your machine: https://docs.docker.com/engine/install/

For PostgreSQL DB docker,
1. Pull docker image
```bash
$ docker pull postgres:alpine
$ docker images # to check what images you have
```

2. Run docker image,
```bash
$ docker run --name fastapi-postgres -e POSTGRES_PASSWORD=password -d -p 5432:5432 postgres:alpine
```

3. Enter into interactive mode with running container,
```bash
$ docker exec -it fastapi-postgres bash
```

4. Start PostgreSQL as a user postgres (superuser, admin),
```bash
$ psql -U postgres
```

5. Create Database, user, grant roles
```psql
postgres=# create database fastapi_db;
postgres=# create user myuser with encrypted password 'password';
postgres=# grant all privileges on database fastapi_db to myuser;
```

6. Connect to fastapi_db and change role to myuser
```psql
postgres=# \c fastapi_db
postgres=# set role myuser;
```

7. Expose docker container to outside(FastAPI application)
```psql
postgres=# psql -h localhost -p 5431 postgres
```



## :computer: Local run

To run the API and front end locally, you will need to have both running in two separate terminal tabs.

In the first tab let's get the API running.

```bash
$ cd backend
$ uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Uvicorn is ASGI web server implementation for python, and 'main:app' is calling an app object that we created within main.py file.
'--reload' enables the restart of the server after code changes. You can navigate to http://127.0.0.1:8000/docs in a browser to see the Swagger spec for the API.

Now open a new terminal tab (Ctrl/Command + T) and get the dash app running:

```bash
$ cd frontend
$ python -m main
```

You should then be able to view the front end application by navigating to http://localhost:8050/ in a browser.


## Containerize your Fastapi application using docker
1. Create Dockerfile and docker-compose.yml
2. Build docker image and run,
```bash
$ docker compose up --build
```