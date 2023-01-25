"""
Custom App Errors
"""
from flask import Blueprint, jsonify
from webargs.flaskparser import parser
from werkzeug.exceptions import NotFound, MethodNotAllowed
from marshmallow import ValidationError
from app.utils import create_logger

logger = create_logger()


class IncorrectArgument(Exception):
    """
    Custom error handling for parsing api arguments

    Based on marshmallow.exceptions.ValidationError
    """

    def __init__(self, message, status_code=422):
        Exception.__init__(self)
        self.message = message
        self.status_code = status_code

    def display_error_message(self):
        """
        Display inherited error messages
        """
        message = self.message.__dict__
        return message["messages"]


# Application error handlers.
errors = Blueprint("errors", __name__)


# Custom Error Function
@parser.error_handler
def handle_error(error, req, schema, status_code, headers):
    """
    Raise error when parsed arguments do not confirm to schema defined in the @parser.use_args(Schema) decorator
    """
    raise IncorrectArgument(error)


@errors.app_errorhandler(Exception)
def handle_unexpected_error(error):
    """
    Error handler for app, customise error messages for specific errors

    """
    # Set default values of response for an unexpected exception
    success = False
    message = [str(x) for x in error.args]
    error_type = error.__class__.__name__
    status_code = 500



    # Overwrite for handled expected exceptions
    if isinstance(error, (IncorrectArgument, ValidationError)):
        # handle when api argument passing fails/ custom errors
        status_code = error.status_code
        message = error.display_error_message()
    elif isinstance(error, NotFound):
        # handle not found response
        status_code = 404
    elif isinstance(error, MethodNotAllowed):
        status_code = 405

    #############################################
    # Exercise 4: add another error handler here
    #############################################

    else:
        # Unexpected exception
        logger.exception(message)
        error_type = "UnexpectedException"
        message = "An unexpected error has occurred."

    # Format a standard Error response, corresponsing to the ErrorResponseSchema
    response = {"success": success, "error": {"type": error_type, "message": message}}

    return jsonify(response), status_code
