"""Main script."""
import logging

from dash import dcc, html

from frontend import submit_stock_level, view_stock_level
from frontend.app import app

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
                        html.H4(children="""Help people find important supplies"""),
                        html.Div(id="dummy", children=None),
                        html.Br(),
                        dcc.Tabs(
                            [
                                submit_stock_level.layout,
                                view_stock_level.layout,
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
