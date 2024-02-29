# API and Frontend

This repository illustrates how to develop APIs and how web applications interact with APIs to retrieve data that user asked for.

For API backend service, we use FastAPI.
For frontend, we use Dash.

## :wrench: Developer set up

First clone the repo. In a terminal, navigate to a folder you want to clone the code to then run:

1. Clone the repo
```bash
$ git clone git@github.com:dustinbaekpersonal/python-api-frontend.git
```

2. Create virtual environment and activate
```bash
python3 -m venv .venv && source .venv/bin/activate
```

3. Install dependencies
```bash
make pip-tools && make pip-tools-dev
```

4. To run pre-commit,
```bash
pre-commit install
```


## :computer: Local run

To run the API and front end locally, you will need to have both running in two separate terminal tabs.

In the first tab let's get the API running.

```bash
$ cd api
$ uvicorn main:app --reload
```

Uvicorn is ASGI web server implementation for python, and 'main:app' is calling an app object that we created within main.py file.
'--reload' enables the restart of the server after code changes. You can navigate to http://127.0.0.1:8000/docs in a browser to see the Swagger spec for the API.

Now open a new terminal tab (Ctrl/Command + T) and get the dash app running:

```bash
$ cd frontend
$ python main.py
```

You should then be able to view the front end application by navigating to http://localhost:8050/ in a browser.
