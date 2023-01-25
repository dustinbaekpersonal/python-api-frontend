# pylint: disable = no-self-use
"""
Define the API endpoints of your applications in this script

Use flasgger to auto produce a OpenAPI-Specification required for your APIs as well as the swagger UI.

WHY?
    1) This will help you produce APIs that are industry standard
    2) Enables you to share the specification of your APIs with others

The examples below generate a swagger spec using the SwaggerView class, where models definitions are constructed using
marshmallow schemas in schema.py.
These examples assume you wish to generate an open api spec from scratch.

Docs: https://github.com/flasgger/flasgger
Example: https://github.com/flasgger/flasgger/blob/master/examples/marshmallow_apispec.py
"""

from flasgger import SwaggerView
from flask import Response, jsonify, request
from webargs.flaskparser import parser

from app.schema import (  # import marshmallow schema objects
    AddressExtended,
    ColourSchema,
    ErrorResponseSchema,
    StandardResponseSchema,
    User,
    StockItemSchema,
    StockLevelReportSchema,
    StockProductTypeSchema,
)

from app.utils import submit_stocklevel, get_stocklevel

# Define the different responses for each error response code experienced by every endpoint
responses = {
    422: {"description": "Incorrect parameter given", "schema": ErrorResponseSchema,},
    400: {"description": "Bad Request", "schema": ErrorResponseSchema},
    500: {"description": "UnexpectedException", "schema": ErrorResponseSchema},
}


# **************************** STOCK LEVEL APIS *****************************


class UpdateStockLevelApi(SwaggerView):
    """
    Json POST API Example

    Update the stock level of a particular store
    """

    # Define swagger definitions needed for Open API Specification
    tags = ["Stock Level"]
    # Input Parameters
    parameters = StockItemSchema

    # DO NOT leave blank, defining the response is ESSENTIAL for collaboration
    responses = {200: {"description": "200 OK", "schema": StandardResponseSchema}}

    # use parser decorator to auto-validate parameters
    @parser.use_args(StockItemSchema)  # default location is json body
    def post(self, payload):
        """
        Add a stock level of an item for a given location
        """
        # json payload (body) in "payload" object
        print(payload)

        # Update the db with
        success = submit_stocklevel(payload)
        ###

        # TEMP response for demo purposes
        response = dict(status=200, message="Stock Successfully Added")
        ###
        return jsonify(response), 200

# EXERCISE 4:
class GetStockLevelReportApi(SwaggerView):
    """
    GET the most recent stock levels for a given product type
    """

    # Define swagger definitions needed for Open API Specification
    tags = ["Stock Level"]
    # Input Parameters
    parameters = [
        {
            "name": "product_type",
            "in": "query",
            "type": "str",
            "description": "product_type",
        },
    ]
    responses = {200: {"description": "200 OK", "schema": StockLevelReportSchema}}

    # use parser decorator to auto-validate parameters
    @parser.use_args(
        StockProductTypeSchema, locations=["querystring"]
    )  # default location is json body, here specify a query string parameter
    def get(self, params):
        """
        GET the most recent stock level report
        """
        # query parameters in "params" object
        print(params)
        product_type = params["product_type"]

        #### Get most recent stock levels for each location
        # exercise 4: finish the get_stocklevel function
        stock_levels = get_stocklevel(product_type)

        response = {"data": stock_levels.to_json(orient="records")}

        return jsonify(response), 200


# ************************************* Example API Types *******************************************
# Each endpoint uses a different type of parameter

class PathParameterExampleApi(SwaggerView):
    """
    Basic Example: GET API with a path parameter

    eg:
    http://mywebsite/api/<uuid>
    where id is a specified path parameter
    """

    # Define swagger definitions needed for Open API Specification
    tags = ["Path Parameter Example"]
    # Input Parameters
    parameters = [
        {
            "name": "uuid",
            "in": "path",
            "required": False,
            "description": "Id of the address in db",
            "type": "uuid",
        },
    ]
    # Extend possible expected response codes for happy path/ additional errors for this specific endpoint
    # DO NOT leave blank, defining the response is ESSENTIAL for collaboration
    responses.update({200: {"description": "200 OK", "schema": AddressExtended}})
    responses = responses  # dictionary

    def get(self, uuid):
        """
        Get the address of a specified ID
        """
        ####
        # INSERT YOUR API BUSINESS LOGIC HERE
        ####

        ###
        # TEMP return for demo purposes
        address = dict(line1="1 New Street Sq", line2="London", city="London")
        result = dict(id=uuid, address=address)
        ###

        return jsonify(result), 200


class JsonPayloadExampleApi(SwaggerView):
    """
    Example: Json Payload POST Example

    eg:
    http://mywebsite/api/create/user

    where the body of the request is json defining the fields required to create a user
    e.g. {"username": "jBlogs", "age": 20}
    """

    # Define swagger definitions needed for Open API Specification
    tags = ["Json Payload Example"]
    # Input Parameters
    parameters = [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": User,  # Marshmallow schema object
        },
    ]
    # Extend possible expected response codes for happy path/ additional errors for this specific endpoint
    # DO NOT leave blank, defining the response is ESSENTIAL for collaboration
    responses.update(
        {
            201: {
                "description": "User created successfully",
                "schema": None,  # Blank response body for 201 HTTP status code
            }
        }
    )
    responses = responses

    # You use flasgger 'inhouse' validation, however it has a limitation to json body parameter only
    # It is recommended to use the @parser.use_args() decorator to validate parameters as it can handle
    # multiple types of parameter and produces a more meaningful error message

    # validation = True  # validation=True forces validation of parameters in body. Can only be used for this kind of parameter.

    # use parser decorator to auto-validate parameters
    @parser.use_args(User)  # default location is json body
    def post(self, user):
        """
        Add User to the DB
        """
        # request.json or user contains json payload User object as defined
        print(user)
        print(request.json)

        ####
        # INSERT YOUR API BUSINESS LOGIC HERE
        ####

        return Response(status=201)  # Temp response for demo purposes


class QueryParameterExampleApi(SwaggerView):
    """
    Basic Example: Single Query Parameter GET API Example

    eg:
    http://mywebsite/api/colour?colour=blue

    where there is a single parameter "colour" set to blue

    """

    # Define swagger definitions needed for Open API Specification
    tags = ["Query Parameter Example"]
    # Input Parameters
    parameters = [
        {
            "name": "colour",
            "in": "query",
            "type": "str",
            "required": False,
            "description": "guess what my favourite colour is",
        },
    ]
    # Extend possible expected response codes for happy path/ additional errors for this specific endpoint
    # DO NOT leave blank, defining the response is ESSENTIAL for collaboration
    responses.update({200: {"description": "200 OK", "schema": StandardResponseSchema}})
    responses = responses

    # use parser decorator to auto-validate parameters
    @parser.use_args(ColourSchema, locations=["querystring"])
    def get(self, args):
        """
        Guess the app's favourite colour
        """
        # Query string parameters in args object
        print(args)

        ####
        # INSERT YOUR API BUSINESS LOGIC HERE
        ####

        ###
        # TEMP response for demo purposes
        response = dict(status=200, message="sorry that isn't my favourite colour")
        ###
        return jsonify(response), 200


class MultiParameterLocationExampleApi(SwaggerView):
    """
    Json & Query Multi Parameter POST API Example

    e.g.
        http://mywebsite/api/colour?colour=blue

    where there is a single query parameter "colour" set to blue AND
    the body of the request is json defining the fields required to create a user
    e.g. {"username": "jBlogs", "age": 20}
    """

    # Define swagger definitions needed for Open API Specification
    tags = ["Json & Query Multi Parameter Example"]
    # Input Parameters
    parameters = [
        {
            "name": "colour",
            "in": "query",
            "type": "str",
            "required": False,
            "description": "guess what my favourite colour is",
        },
        {
            "name": "body",
            "in": "body",
            "required": True,
            "description": "Description",
            "schema": User,
        },
    ]
    # Extend possible expected response codes for happy path/ additional errors for this specific endpoint
    # DO NOT leave blank, defining the response is ESSENTIAL for collaboration
    responses.update({200: {"description": "200 OK", "schema": StandardResponseSchema}})
    responses = responses
    # validation = True  # cannot use with multiple parameter locations

    # use parser decorator to auto-validate parameters
    @parser.use_args(ColourSchema, locations=["querystring"])
    @parser.use_args(User)  # default location is json body
    def post(self, params, payload):
        """
        add a user & their favourite colour
        """
        # query string parameters in "args" object
        print(params)
        # json payload (body) in "payload" object
        print(payload)

        ####
        # INSERT YOUR API BUSINESS LOGIC HERE
        ####

        ###
        # TEMP response for demo purposes
        response = dict(
            status=200, message="check the app logs to see all input parameter objects"
        )
        ###
        return jsonify(response), 200
