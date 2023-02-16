import logging

import dash

logger = logging.getLogger(__name__)
logging.basicConfig(
    format="%(asctime)s : %(levelname)s : %(message)s",
    datefmt="%d/%m/%Y %H:%M:%S",
    level="DEBUG",
)

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]


app = dash.Dash(
    __name__,
    meta_tags=[
        {
            "name": "viewport",
            "content": "width=device-width,initial-scale=1,shrink-to-fit=no",
        }
    ],
)

app.title = "PaperTrail"

app.config.suppress_callback_exceptions = True
