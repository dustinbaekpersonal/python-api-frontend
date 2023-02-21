import logging
from datetime import datetime

import dash_bootstrap_components as dbc
import requests
import yaml
from app import app

from dash import dcc, html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

with open("../config.yml", "r") as stream:
    config = yaml.safe_load(stream)

logger = logging.getLogger(__name__)
logging.basicConfig(
    format="%(asctime)s : %(levelname)s : %(message)s", datefmt="%d/%m/%Y %H:%M:%S", level="DEBUG",
)

layout = dcc.Tab(
    label="Report stock levels",
    children=[
        html.Br(),
        html.H2("Report stock levels in a store near you"),
        dbc.Row(
            dbc.Col(
                [
                    html.Label("Product type"),
                    dcc.Dropdown(
                        id="product_input",
                        options=[{"label": p.title(), "value": p} for p in config["products"]],
                        placeholder="Select stock type",
                        searchable=False,
                    ),
                ],
                width=6,
            )
        ),
        dbc.Row(
            dbc.Col(
                [
                    html.Br(),
                    html.Label("Stock level"),
                    html.Br(),
                    dcc.Input(id="stock_level_input", type="number", placeholder="Enter stock level", min=0,),
                ],
                width=6,
            )
        ),
        dbc.Row(
            dbc.Col(
                [
                    html.Br(),
                    html.Label("Store name"),
                    html.Br(),
                    dcc.Dropdown(
                        id="store_input",
                        options=[{"label": store, "value": store,} for store in config["stores"]],
                        placeholder="Select store name",
                        searchable=False,
                    ),
                ],
                width=6,
            )
        ),
        html.Br(),
        html.Button("Submit", id="submit_button"),
        html.Br(),
        html.Div(id="submit_confirmation"),
    ],
)


@app.callback(
    Output("submit_confirmation", "children"),
    [Input("submit_button", "n_clicks")],
    [State("product_input", "value"), State("store_input", "value"), State("stock_level_input", "value"),],
)
def submit_stocklevel(n_clicks, product, store, stock_level):
    """
    Submit stock level to fastapi

    Parameters
    ----------
    n_clicks : int
        Number of clicks on submit button
    product : str
        Product name
    store : str
        Store name
    stock_level : int
        Stock level

    Returns
    -------
    str
        Confirmation message

    Raises
    ------
    PreventUpdate
        If n_clicks is 0
    """
    if not n_clicks:
        raise PreventUpdate

    url = f"{config['fastapi_url']}/submit-stocklevel"

    data = {
        "product": product,
        "store": store,
        "stock_level": stock_level,
        "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    logger.info(f"Sending stock level to {url} with data: {data}")
    req = requests.post(url, json=data)
    if req.status_code != 200:
        logger.error(f"Error submitting stock level: {req.text}")
        raise PreventUpdate

    return f"Thanks for submitting the {product.title()} stock level at {store}!"
