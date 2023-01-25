import logging
import os
import platform
from datetime import datetime

import dash
import dash_core_components as dcc
import dash_html_components as html
import geocoder
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import requests
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from flask import request

from app import app
from config import config

API_KEY = config["API_KEY"]

logger = logging.getLogger(__name__)
logging.basicConfig(
    format="%(asctime)s : %(levelname)s : %(message)s",
    datefmt="%d/%m/%Y %H:%M:%S",
    level="DEBUG",
)


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
                                html.Label("Store location"),
                            ],
                            className="row",
                            style={"padding-left": "15px"},
                        ),
                        html.Div(
                            [
                                dcc.Input(
                                    id="address_input_box",
                                    type="text",
                                    placeholder="Location",
                                    style={
                                        "width": "100%",
                                        "margin-right": "15px",
                                    },
                                ),
                            ],
                            className="row",
                            style={"padding-left": "15px"},
                        ),
                        html.Div(
                            "Please click to check the store address before submitting",
                            style={"padding": "15px 0px 0px 0px"},
                        ),
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.Button(
                                            "Check address", id="address_preview_button"
                                        ),
                                    ],
                                    className="col-6",
                                    style={"padding": "15px 0px 0px 15px"},
                                ),
                                html.Div(
                                    [
                                        html.Button(
                                            "Submit", id="submit_button", n_clicks=0
                                        ),
                                    ],
                                    className="col-6",
                                    style={"padding": "15px 0px 0px 15px"},
                                ),
                            ],
                            className="row justify-content-between",
                        ),
                        html.Div(
                            [
                                html.Div(id="address_preview"),
                            ],
                            className="row",
                            style={"padding": "15px 0px 0px 15px"},
                        ),
                        html.Div(
                            id="check_address_map_container",
                            children=[dcc.Graph(id="check_address_map")],
                            hidden=True,
                        ),
                    ],
                    className="col-12 col-md-6",
                )
            ],
            className="row justify-content-md-left",
        ),
        html.Br(),
        html.Div(id="submit_confirmation_div"),
    ],
)


@app.callback(
    [
        Output("address_preview", "children"),
        Output("address_response_store", "data"),
        Output("check_address_map_container", "hidden"),
        Output("check_address_map", "figure"),
    ],
    [Input("address_preview_button", "n_clicks")],
    [State("address_input_box", "value")],
)
def check_address(n_clicks, input_address):
    """Check that the address the user entered actually resolves
    to a real shop, and that it's the right one

    Args:
            n_clicks      (int): Number of times the "check address" button has been clicked
            input_address (str): Raw address input from the user

    Returns:
            preview_str (str): Comment to display to the user, containing the resolved address
            response   (dict): Response from the geocoder API
            False      (bool): Unhides the map
            Map data   (dict): Data to be used to plot the map

    """
    if not n_clicks:
        raise PreventUpdate

    # Ping the Geocoder API to get the lat,long for the user's address
    response = query_geocoder(input_address)

    if response["status"] != "ok":
        raise PreventUpdate
        ### Log this

    preview_str = (
        f"Please check this is the right store address: {response['resolved_address']}"
    )

    ### Generate map figure showing the target location:
    map_data = go.Scattermapbox(
        lat=[response["lat"]],
        lon=[response["lng"]],
        mode="markers",
        marker=dict(
            size=15,
            color="blue",
        ),
        hovertext=response["resolved_address"],
    )

    # Define the plotly graph object to plot
    map_layout = go.Layout(
        mapbox_style="open-street-map",
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        mapbox=dict(
            center=go.layout.mapbox.Center(
                lat=response["lat"],
                lon=response["lng"],
            ),
            zoom=15,
        ),
        height=250,
    )

    return preview_str, response, False, {"data": [map_data], "layout": map_layout}


def query_geocoder(address):
    """
    Send the user's address to Google's Geocoder API, and return the response.

    Args:
            address (str): Raw address input from the user
    Returns:
            response (dict): Response from the API
    """

    base_url = "https://maps.googleapis.com/maps/api/geocode/json"

    params = {"address": address, "key": API_KEY}

    # Issue the API request
    logger.info("making request with params: %s", params)
    results = requests.get(base_url, params=params)

    results = results.json()

    # Check the query worked OK
    if results["status"] != "OK":
        logger.error("ERROR: Geocoder failed")
        logger.debug("Geocoder status: ", results["status"])
        return {"status": "failed"}

    # Parse out the bits we need
    results = results["results"][0]
    lat = results["geometry"]["location"]["lat"]
    lng = results["geometry"]["location"]["lng"]

    geocode = f"{lat},{lng}"

    resolved_address = results["formatted_address"]

    place_id = results["place_id"]

    logger.debug(
        f"Address '%s' resolved to '%s' at geocode (%s)",
        address,
        resolved_address,
        geocode,
    )

    # Create the response to return to the app
    response = {
        "status": "ok",
        "input_address": address,
        "lat": lat,
        "lng": lng,
        "geocode": geocode,
        "resolved_address": resolved_address,
        "place_id": place_id,
    }

    return response


@app.callback(
    Output("submit_confirmation_div", "children"),
    [Input("submit_button", "n_clicks")],
    [
        State("product_type_input_dropdown", "value"),
        State("stock_level_dropdown", "value"),
        State("address_input_box", "value"),
        State("address_response_store", "data"),
    ],
)

def submit_stocklevel(n_clicks, product_type, stock_level, input_address, address_response):
    """Using our user's inputs of stock type & level, as well as the resolved address,
    put the stock report somewhere. In this case, we'll send it to our API!

    Args:
            n_clicks (int): Number of clicks of the submit button
            product_type (str): Product type being reported
            stock_level (int):
            input_address
            address_response

    Returns:
            str: Confirmation response to display on the screen to the user

    """
    if not n_clicks or not input_address:
        raise PreventUpdate

    if not address_response:
        response = query_geocoder(input_address)
    else:
        response = address_response


    url = f"{config['FLASK_APP_URL']}/api/v1/stocklevel"

    data = {
        "input_address": response["input_address"],
        "resolved_address": response["resolved_address"],
        "geocode": response["geocode"],
        "lat": str(response["lat"]),
        "lng": str(response["lng"]),
        "stock_level": stock_level,
        "product_type": product_type,
        "datetime": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
    }

    # Make request to flask-app to add stock
    req = requests.post(url, json=data)
    if req.status_code != 200:
        # raise error
        raise PreventUpdate


    return f"Thanks for submitting the {product_type} stock level at {response['resolved_address']}!"
