import logging
import os
import platform
import requests

import dash_core_components as dcc
import dash_html_components as html
import dash_table
import geocoder
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from flask import request

from app import app
from config import config

logger = logging.getLogger(__name__)
logging.basicConfig(
    format="%(asctime)s : %(levelname)s : %(message)s",
    datefmt="%d/%m/%Y %H:%M:%S",
    level="DEBUG",
)


layout = dcc.Tab(
    label="View local stock levels",
    children=[
        html.Br(),
        html.H2("View local stock levels"),
        html.Label("Product type"),
        # Select the stock to view levels of
        dcc.Dropdown(
            id="product_type_mapview_dropdown",
            options=[
                {"label": p.title(), "value": p.replace(" ", "_")}
                for p in config["product_types"]
            ],
            value="toilet_paper",
            placeholder="Select stock type",
            searchable=False,
        ),
        html.Br(),
        # This container holds the map - it will be populated by draw_map
        html.Div(
            id="map_container",
            children=[dcc.Graph(id="map_map")],
        ),


        ########################################
        #### Insert your reports table here ####
        ########################################
        html.Br(),
        html.Div(
            id="reports_table_div",
            children=[
                dash_table.DataTable(
                    id="reports_table",
                    style_as_list_view=True,
                    style_data={"fontFamily": "lato, sans-serif"},
                    style_header={
                        "fontFamily": "lato, sans-serif",
                        "padding": "0px 2px",
                        "backgroundColor": "rgba(208, 208, 206, 0.5)",
                    },
                    style_cell={"textAlign": "left"},
                    page_size=10,
                    style_data_conditional=[
                        {
                            "if": {"row_index": "odd"},
                            "backgroundColor": "rgba(208, 208, 206, 0.2)",
                        }
                    ],
                    style_table={
                        "overflowX": "scroll",
                        "padding-left": "15px",
                    },
                )
            ],
        ),
    ],
)


@app.callback(
    [Output("reports_table", "data"), Output("reports_table", "columns")],
    [Input("product_type_mapview_dropdown", "value")],
)
def populate_results_table(product_type):
    """
    For a given product_type, populate a table with the most recent reports

    Args:
            product_type (str): Product type for which to display the results
    Returns:
            dict: Data for the data table, in dict form
            list: Columns for the table
    """

    reports_df = load_reports(product_type)
    logger.info("Loaded results df, with %s rows", len(reports_df))

    return_dict = reports_df[["resolved_address", "stock_level", "datetime"]].to_dict(
        "records"
    )
    columns = [
        {"name": i, "id": i} for i in ["resolved_address", "stock_level", "datetime"]
    ]

    return return_dict, columns


def load_reports(product_type):
    """For a given product_type, returns the most recent stock level for each location

    Args:
            product_type (str): product type for which to return the results
    Returns:
            reports_df (pd.DataFrame): DataFrame of the results for the given product_type

    """

    url = f"{config['FLASK_APP_URL']}/api/v1/stocklevel"
    # Make request to flask-app to add stock


    req = requests.get(url, params=dict(product_type=product_type))
    if req.status_code != 200:
        # create blank df
        reports_df = pd.DataFrame(
            columns=["datetime", "resolved_address", "lat", "lng", "stock_level"]
        )
    else:

        data = req.json()["data"]
        # get df data from request payload
        reports_df = pd.read_json(data, orient="records")


    return reports_df


@app.callback(
    Output("map_map", "figure"),
    [
        Input("product_type_mapview_dropdown", "value"),
    ],
)
def draw_map(product_type):
    """Produces the plotly graph object to display the most recent
    reports for each location of a given stock, centred to the user's location

    Args:
            product_type (str): product type for which to display stock levels

    Returns:
            dict (plotly.graphobject.Scattermapbox, plotly.graphobject.Layout): Plotly objects required to plot the map

    """

    logger.debug("Load map button clicked! ")

    ### Replace this line with a new GET request to our API ###
    reports_df = load_reports(product_type)
    logger.info("Loaded results df, with %s rows", len(reports_df))

    map_data = go.Scattermapbox(
        lat=reports_df["lat"],
        lon=reports_df["lng"],
        mode="markers",
        marker=dict(
            size=15,
            showscale=True,
            color=reports_df["stock_level"],
            cmin=0,
            cmax=3,
            colorscale=["black", "red", "orange", "green"],
            colorbar=dict(
                title="Stock level",
                tickmode="array",
                tickvals=[0, 1, 2, 3],
                ticktext=["Out of stock", "Low", "Medium", "High"],
                ticks="outside",
                thicknessmode="fraction",
                thickness=0.03,
            ),
        ),
        hovertext=reports_df["resolved_address"]
        + "<br>Last reported: "
        + reports_df["datetime"],
    )

    client_ip = "me"

    logger.debug("IP for localisation: %s", client_ip)

    # Get the IP address to centre the map
    curr_loc = geocoder.ip(client_ip).latlng

    logger.debug("Geocoded location from IP: %s", curr_loc)

    map_layout = go.Layout(
        mapbox_style="open-street-map",
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        mapbox=dict(
            center=go.layout.mapbox.Center(lat=curr_loc[0], lon=curr_loc[1]),
            zoom=10,
        ),
    )

    return {"data": [map_data], "layout": map_layout}
