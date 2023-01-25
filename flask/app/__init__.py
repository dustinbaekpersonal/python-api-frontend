"""
app/__init__.py

initialise flask app object
"""
import os

from flasgger import Swagger
from flask import Flask, Blueprint

from app.api import (
    PathParameterExampleApi,
    JsonPayloadExampleApi,
    QueryParameterExampleApi,
    MultiParameterLocationExampleApi,
    UpdateStockLevelApi,
    GetStockLevelReportApi,
)  # Import defined endpoints created using SwaggerView class
from app.errors import (
    errors,
)  # import blueprint containing error handler for application


def _register_endpoints(app: Flask):
    """
    Register all endpoints for this application

    Register the endpoints in __init__ to avoid circular references
    """
    api_v1 = Blueprint('api_v1', __name__, url_prefix='/api/v1')

    # Define routes for stock level endpoints
    api_v1.add_url_rule(
        "/stocklevel",
        view_func=UpdateStockLevelApi.as_view("UpdateStockLevelApi"),
        methods=["POST"],
    )
    #############################################
    # Exercise 4: Add GetStockLevelReportApi endpoint ROUTE here
    #############################################





    # Define routes for example endpoints
    api_v1.add_url_rule(
        "/address/<string:uuid>",
        view_func=PathParameterExampleApi.as_view("PathParameterExampleApi"),
        methods=["GET"],
    )
    api_v1.add_url_rule(
        "/user/add",
        view_func=JsonPayloadExampleApi.as_view("JsonPayloadExampleApi"),
        methods=["POST"],
    )
    api_v1.add_url_rule(
        "/colour/guess",
        view_func=QueryParameterExampleApi.as_view("QueryParameterExampleApi"),
        methods=["GET"],
    )
    api_v1.add_url_rule(
        "/colour/user",
        view_func=MultiParameterLocationExampleApi.as_view(
            "MultiParameterLocationExampleApi"
        ),
        methods=["POST"],
    )

    # Register api_v1 blueprint
    app.register_blueprint(api_v1)

def _initialize_errorhandlers(app: Flask):
    """
    Initialize error handlers

    Use a blueprint so that you can define application error handlers without circular references
    """
    # register error handler blueprint
    app.register_blueprint(errors)


def create_app() -> Flask:
    """
    Create an app by initializing components.

    args:
        None

    returns:
        app (Flask): Flask app object
    """

    # Create Flask App object
    app = Flask(__name__)  # pylint: disable = invalid-name

    # Get Flask App config based on environment variable
    config_env = "config.{}Config".format(
        os.getenv("ENV", "Dev")
    )  # config object as defined in config.py
    app.config.from_object(config_env)  # Set to chosen configs

    # Swagger Documentation Settings, enable autodocumentation of your APIs
    # produces swagger api webpage under {app_url}/swagger, locally: http://0.0.0.0:5000/swagger (urls can be configured on settings see: https://github.com/flasgger/flasgger
    # full json spec found under {app_url}/apispec_1.json, locally: http://0.0.0.0:5000/apispec_1.json
    swagger = Swagger(app)  # pylint: disable = unused-variable

    # Add endpoints to application object
    _register_endpoints(app)

    # initialise error handlers
    _initialize_errorhandlers(app)

    return app
