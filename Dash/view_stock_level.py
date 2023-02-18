import json
import logging

import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import requests
import yaml
from app import app

from dash import dcc, html
from dash.dependencies import Input, Output

with open("../config.yml", "r") as stream:
    config = yaml.safe_load(stream)


logger = logging.getLogger(__name__)
logging.basicConfig(
    format="%(asctime)s : %(levelname)s : %(message)s",
    datefmt="%d/%m/%Y %H:%M:%S",
    level="DEBUG",
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
            options=[{"label": p.title(), "value": p} for p in config["product_types"]],
            value= config["product_types"][0],
            placeholder="Select stock type",
            searchable=False,
        ),
        html.Br(),
        html.Div(
            id="example-graph-2",
            children=[dcc.Graph(id="pd_df")],
        ),
    ],
)


def load_reports(product_type):
    """For a given product_type, returns the most recent stock level for each location
    Args:
            product_type (str): product type for which to return the results
    Returns:
            reports_df (pd.DataFrame): DataFrame of the results for the given product_type
    """

    url = f"{config['fastapi_url']}/get-by-product-name"

    req = requests.get(url, params=dict(product_type=product_type))
    if req.status_code != 200:
        reports_df = pd.DataFrame(columns=["store_name", "product_type", "stock_level", "datetime"])
    else:
        data = req.json()
        data_json = json.dumps(data)
        reports_df = pd.read_json(data_json, orient="records")
    return reports_df


@app.callback(
    Output("pd_df", "figure"),
    [
        Input("product_type_dropdown", "value"),
    ],
)
def draw_graph(product_type):
    reports_df = load_reports(product_type)
    if reports_df.empty:
        fig = go.Figure()
        fig.update_layout(
            xaxis={"visible": False},
            yaxis={"visible": False},
            annotations=[
                {
                    "text": "No matching product type found in any stores",
                    "xref": "paper",
                    "yref": "paper",
                    "showarrow": False,
                    "font": {"size": 28},
                }
            ],
        )
    else:
        fig = px.bar(reports_df, x="store_name", y="stock_level", color="store_name",
                     title=f"Stock Level of {product_type.title()} by Stores",
                     labels={ "store_name":"Store Name", "stock_level":"Stock Level"})
    return fig
