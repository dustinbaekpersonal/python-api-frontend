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
$ cd fastapi/app
$ uvicorn main:app --reload
```

Uvicorn is ASGI web server implementation for python, and 'main:app' is calling an app object that we created within main.py file. 
'--reload' enables the restart of the server after code changes. You can navigate to http://127.0.0.1:8000/docs in a browser to see the Swagger spec for the API.

Now open a new terminal tab (Ctrl/Command + T) and get the dash app running:

```bash
$ conda activate fastapi-dash-training
$ cd dash
$ python main.py
```

You should then be able to view the front end application by navigating to http://0.0.0.0:8050/ in a browser.

# Python based Web Framework API using FastAPI

This repository is the starting point for FastAPI and Dash course. It contains how to build an API and micro web framework using FastAPI and build a front-end web framework using Dash.
Here you can:
* Learn what API is
* Learn RESTful API methods for HTTP
* Learn how to define & parse API arguments
* Learn how to handle the error (e.g. Server Response code: 2xx, 4xx, 5xx)
* Learn the perks of using FastAPI(e.g.Auto-Documentation of APIs using Swagger, Auto-validation)

## Examples
These APIs are based off: https://fastapi.tiangolo.com/tutorial/

## Useful Links
What is API?: https://aws.amazon.com/what-is/api/

