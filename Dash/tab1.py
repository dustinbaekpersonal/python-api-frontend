import logging
import os
import platform
from datetime import datetime

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import requests
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
#from flask import request

from app import app
from config import config

logger = logging.getLogger(__name__)
logging.basicConfig(
    format="%(asctime)s : %(levelname)s : %(message)s",
    datefmt="%d/%m/%Y %H:%M:%S",
    level="DEBUG",
)

# To  create a tab section for product types, stock levels and store names
layout = dcc.Tab(
    label="Report stock levels",
    children=[
        html.Br(),
        html.H2("Report stock levels in a store near you"),
        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                html.Label("Product type"),
                            ],
                        ),
                        html.Div(
                            [
                                dcc.Dropdown(
                                    id="product_type_input_dropdown",
                                    options=[
                                        {
                                            "label": p.title(),
                                            "value": p.replace(" ", "_"),
                                        }
                                        for p in config["product_types"]
                                    ],
                                    value="toilet_paper",
                                    placeholder="Select stock type",
                                    searchable=False,
                                ),
                            ],
                        ),
                    ],
                    className="col-12 col-md-6",
                ),
            ],
            className="row justify-content-md-left",
        ),
        html.Br(),
        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                html.Label("Stock level"),
                            ],
                        ),
                        html.Div(
                            [
                                dcc.Dropdown(
                                    id="stock_level_dropdown",
                                    options=[
                                        {"label": "High", "value": 3},
                                        {"label": "Medium", "value": 2},
                                        {"label": "Low", "value": 1},
                                        {"label": "Out of stock", "value": 0},
                                    ],
                                    value=None,
                                    placeholder="Select stock level",
                                    searchable=False,
                                ),
                            ],
                        ),
                    ],
                    className="col-12 col-md-6",
                ),
            ],
            className="row justify-content-md-left",
        ),
        html.Br(),
        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                html.Label("Store name"),
                            ],
                        ),
                        html.Div(
                            [
                                dcc.Dropdown(
                                   id =  "store_name_dropdown",
                                   options =[
                                       {
                                        "label": p.title(),
                                        "value": p.replace(" ", "_"), 
                                       }
                                   for p in config["store_names"]
                                    ],
                                  value="Sainsbury_Euston",
                                  placeholder="Select store name",
                                  searchable=False,
                                ),
                            ],
                        ),    
                    ],  
                    className="col-12 col-md-6"
                ),
            ], 
            className="row justify-content-md-left",   
        ),
       html.Br(),
       html.Div(id="submit_confirmation_div"),
    ],

)

# This section calls back (i.e. activates the change in input) the values of the sections - product type, stock level and store names into the app

@app.callback(
    Output("submit_confirmation_div", "children"),
    [Input("submit_button", "n_clicks")],
    [
        State("product_type_input_dropdown", "value"),
        State("stock_level_dropdown", "value"),
        State("store_name_dropdown", "value"),
        State("address_response_store", "data"),
    ],
)

def submit_stocklevel(n_clicks, product_type, stock_level, store_name, address_response):
    """Using our user's inputs of stock type & level, as well as the resolved address,
    put the stock report somewhere. In this case, we'll send it to our API!
    Args:
            n_clicks (int): Number of clicks of the submit button
            product_type (str): Product type being reported
            stock_level (int):
            store_name (str):
            address_response
    Returns:
            str: Confirmation response to display on the screen to the user
    """
    if not n_clicks or not input_address:
        raise PreventUpdate

    item_id="ZG011AQA"
    url = f"{config['FastAPI_APP_URL']}/create-stocklevel/{item_id}"

    data = {
        "stock_level": stock_level,
        "product_type": product_type,
        "store_name": store_name,
        "datetime": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
    }

    # Make request to FAST-app to add stock
    req = requests.post(url, json=data)
    if req.status_code != 200:
        raise PreventUpdate


    return f"Thanks for submitting the {product_type} stock level at {response['resolved_address']}!"