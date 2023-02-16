# Python based Web Framework API using FastAPI

This repository is the starting point for FastAPI and Dash course. It contains how to build an API and micro web framework using FastAPI and build a front-end web framework using Dash.
Here you can:
* Learn what API is
* Learn RESTful API methods for HTTP
* Learn how to define & parse API arguments
* Learn how to handle the error (e.g. Server Response code: 2xx, 4xx, 5xx)
* Learn the perks of using FastAPI(e.g.Auto-Documentation of APIs using Swagger, Auto-validation)

## Set Up

### Code

First clone the repo. In a terminal, use the following commands:
```
# change directory to the folder you want to clone repo in, e.g. Documents/code shown below
cd Documents/code
# Use HTTPS or SSH 
git clone https://github.com/danalyticsuk/python-api-frontend-training.git
# git clone git@github.com:danalyticsuk/python-api-frontend-training.git
cd FastAPI
```

Next make sure you have the dependencies installed. For this, we will create virtual environment first.

Consider creating a virtual environment using conda:
```
# create conda venv
conda create -n fastapi python=3.7
# activate venv
conda activate fastapi
```

Install dependencies
```
pip install -r requirements.txt
```

## Usage

To run the the main.py file:

```
# change directory to app§
cd app
# run main.py using uvicorn
uvicorn main:app --reload
```

Uvicorn is ASGI web server implementation for python, and 'main:app' is calling an app object that we created within main.py file. 
'--reload' enables the restart of the server after code changes.


## Examples
These APIs are based off: https://fastapi.tiangolo.com/tutorial/

## Useful Links
What is API?: https://aws.amazon.com/what-is/api/

