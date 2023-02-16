import logging
import os
import platform
import requests
import json
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
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

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

layout = dcc.Tab(
    label="View local stock levels",
    children=[
        html.Br(),
        html.H2("View local stock levels"),
        html.Label("Product type"),
        dcc.Dropdown(
            id="product_type_dropdown",
            options=[
                {"label": p.title(), "value": p.replace(" ", "_")}
                for p in config["product_types"]
            ],
            value="toilet_paper",
            placeholder="Select stock type",
            searchable=False,
        ),
        html.Br(),
        html.Div(
            id="example-graph-2",
            children=[dcc.Graph(id="pd_df")],
        )
    ]
)




def load_reports(product_type):
    """For a given product_type, returns the most recent stock level for each location
    Args:
            product_type (str): product type for which to return the results
    Returns:
            reports_df (pd.DataFrame): DataFrame of the results for the given product_type
    """

    url = f"{config['FastAPI_APP_URL']}/get-by-product-name"
   
    req = requests.get(url, params=dict(product_type=product_type))
    if req.status_code != 200:
        # create blank df
        reports_df = pd.DataFrame(
            columns=["store_name","product_type","stock_level","datetime"]
        )
    else:
        data = req.json()
        data_json = json.dumps(data)

        # # get df data from request payload
        reports_df = pd.read_json(data_json, orient="records")


    return reports_df

@app.callback(Output("pd_df", "figure"),
    [
        Input("product_type_dropdown", "value"),
    ]
)
def draw_graph(product_type):
    reports_df = load_reports(product_type)
    if reports_df.empty:
        fig = go.Figure()
        fig.update_layout(
            xaxis =  { "visible": False },
            yaxis = { "visible": False },
            annotations = [
                {   
                    "text": "No matching product type found in any stores",
                    "xref": "paper",
                    "yref": "paper",
                    "showarrow": False,
                    "font": {
                        "size": 28
                    }
                }
            ]
        )
    else:
        fig = px.bar(reports_df, x="store_name", y="stock_level", color="store_name")
    return fig


