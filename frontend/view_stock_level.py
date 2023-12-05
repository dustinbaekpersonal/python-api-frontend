import logging

import pandas as pd
import plotly.express as px
import requests
import yaml
from app import app
from dash import dcc, html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

with open("../config.yml", "r") as stream:
    config = yaml.safe_load(stream)


logger = logging.getLogger(__name__)
logging.basicConfig(
    format="%(asctime)s : %(levelname)s : %(message)s", datefmt="%d/%m/%Y %H:%M:%S", level="DEBUG",
)

colors = {"background": "#111111", "text": "#7FDBFF"}

layout = dcc.Tab(
    label="View local stock levels",
    children=[
        html.Br(),
        html.H2("View local stock levels"),
        html.Label("Product type"),
        dcc.Dropdown(
            id="product_type_dropdown",
            options=[{"label": p.title(), "value": p} for p in config["products"]],
            value=config["products"][0],
            searchable=False,
        ),
        html.Br(),
        html.Div([dcc.Graph(id="bar_chart")],),
    ],
)


@app.callback(
    Output("bar_chart", "figure"), [Input("product_type_dropdown", "value"),],
)
def draw_graph(product: str) -> px.bar:
    """Draw a bar chart of the stock level of a product in each store.

    Parameters
    ----------
    product : str
        product name

    Returns:
    -------
    Plotly Figure
        bar chart of the stock level of a product in each store

    Raises:
    ------
    PreventUpdate
        When the API call fails
    """
    url = f"{config['fastapi_url']}/stock-levels"
    logger.info(f"Calling {url} with product={product}")
    response = requests.get(url, params={"product": product})
    if response.status_code == 200:
        data_df = pd.DataFrame(response.json())
        fig = px.bar(
            data_df,
            x=data_df.index,
            y="stock_level",
            title=f"Stock Level of {product.title()} by store",
            labels={"stock_level": "Stock Level", "index": "Store"},
        )
        return fig
    else:
        logger.error(f"Error calling {url}: {response.status_code} {response.text}")
        raise PreventUpdate
