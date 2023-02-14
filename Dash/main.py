import logging

import dash_core_components as dcc
import dash_html_components as html

import tab1
import tab2
from app import app


logger = logging.getLogger(__name__)
logging.basicConfig(
    format="%(asctime)s : %(levelname)s : %(message)s",
    datefmt="%d/%m/%Y %H:%M:%S",
    level="DEBUG",
)


app.layout = html.Div(
    children=[
        html.Div(
            [
                html.Div(
                    children=[
                        html.H1(children="PaperTrail"),
                        html.H4(
                            children="""Help people find important supplies"""
                        ),
                        # This dummy div is a bit of a hack to let us fire callbacks
                        # on page load
                        html.Div(id="dummy", children=None),
                        # We will store the response from the Geocoder API in this dcc.Store component
                        #dcc.Store(id="address_response_store", storage_type="memory"),
                        html.Br(),
                        # The main body of the page is split over two tabs
                        # To keep this file less cluttered, they are defined in their own .py files.
                        dcc.Tabs(
                            [
                                # Tab 1 is the "Report Stock Levels" tab
                                tab1.layout,
                                # Tab 2 is "View Local Stock Levels"
                                tab2.layout,
                            ]
                        ),
                        html.Div(style={"height": "50%"}),
                        html.Footer("Icon made by Freepik from www.flaticon.com"),
                    ],
                    className="col-12",
                )
            ],
            className="row justify-content-md-center",
        ),
    ],
    className="container",
)


if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=8050, debug=True)
