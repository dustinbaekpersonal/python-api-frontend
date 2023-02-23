# FastAPI and Dash training

Welcome to the FastAPI and Dash training! 

## :wrench: Developer set up

To take part in the training course you will need to clone this repository and set up the local development environment. 

First clone the repo. In a terminal, navigate to a folder you want to clone the code to then run:

```bash
$ git clone https://github.com/danalyticsuk/python-api-frontend-training.git
```

We will use conda for the virtual environment for this training. To get this set up, you will need to have anaconda already installed on your machine. To set it up and activate run:

```bash
$ conda env create -f environment.yml
$ conda activate fastapi-dash-training
```

## :computer: Local run

To run the API and front end locally, you will need to have both running in two separate terminal tabs. 

In the first tab let's get the API running. 

```bash
$ cd FastAPI
$ uvicorn main:app --reload
```

Uvicorn is ASGI web server implementation for python, and 'main:app' is calling an app object that we created within main.py file. 
'--reload' enables the restart of the server after code changes. You can navigate to http://127.0.0.1:8000/docs in a browser to see the Swagger spec for the API.

Now open a new terminal tab (Ctrl/Command + T) and get the dash app running:

```bash
$ conda activate fastapi-dash-training
$ cd Dash
$ python main.py
```

You should then be able to view the front end application by navigating to http://localhost:8050/ in a browser.
