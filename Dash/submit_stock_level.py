import logging
import random
import string
import yaml

import requests

from app import app

from dash import dcc, html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

with open("../config.yml", 'r') as stream:
    config = yaml.safe_load(stream)

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
                                        {"label": value, "value": value}
                                        for value in config["stock_levels"]
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
                                    id="store_name_dropdown",
                                    options=[
                                        {
                                            "label": p,
                                            "value": p,
                                        }
                                        for p in config["store_names"]
                                    ],
                                    value=config["store_names"][0],
                                    placeholder="Select store name",
                                    searchable=False,
                                ),
                            ],
                        ),
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.Button("Submit", id="submit_button", n_clicks=1),
                                    ],
                                    className="col-6",
                                    style={"padding": "15px 0px 0px 15px"},
                                ),
                            ],
                            className="row justify-content-between",
                        ),
                    ],
                    className="col-12 col-md-6",
                ),
            ],
            className="row justify-content-md-left",
        ),
        html.Br(),
        html.Div(id="submit_confirmation_div"),
    ],
)

# not a very smart way, but whenever we create stocklevel, we need to input unique SKU id. For that we will randomly genearte 8 digits, so that front end users don't need to worry about it.
def id_generator(size=8, char=string.ascii_uppercase + string.digits):
    return "".join([random.choice(char) for _ in range(size)])


# This section calls back (i.e. activates the change in input) the values of the sections - product type, stock level and store names into the app


@app.callback(
    Output("submit_confirmation_div", "children"),
    [Input("submit_button", "n_clicks")],
    [
        State("product_type_input_dropdown", "value"),
        State("stock_level_dropdown", "value"),
        State("store_name_dropdown", "value"),
    ],
)
def submit_stocklevel(n_clicks, product_type, stock_level, store_name):
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
    if not n_clicks:
        raise PreventUpdate

    item_id = id_generator()  # randomly generate SKU for every submit
    url = f"{config['fastapi_url']}/create-stocklevel/{item_id}"

    data = {
        "stock_level": stock_level,
        "product_type": product_type,
        "store_name": store_name,
    }

    # Make request to FAST-app to add stock
    req = requests.post(url, json=data)
    if req.status_code != 200:
        raise PreventUpdate

    return f"Thanks for submitting the {product_type} stock level at {store_name}!"
