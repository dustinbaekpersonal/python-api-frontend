# pylint: disable=too-few-public-methods
"""
This script defines the schemas of the models of the API inputs/ outputs using Marshmallow

https://marshmallow.readthedocs.io/en/stable/quickstart.html
"""
from marshmallow import INCLUDE, Schema, fields, validate


class ColourSchema(Schema):
    """
    Schema for favorite colour API
    """

    colour = fields.Str(required=True)


class IdSchema(Schema):
    """
    Schema for api input when a customer wishes to recategorise a transaction
    """

    uuid = fields.UUID(required=True)


class SimpleAddress(Schema):
    """
    Schema of simple address
    """

    line1 = fields.Str(
        required=True, validate=[validate.Length(min=1, error="Must be non-empty")]
    )
    line2 = fields.Str(required=False)
    city = fields.Str(required=True)


class AddressExtended(Schema):
    """
    Schema with nested dictionary
    """

    id = fields.UUID(required=True)
    address = fields.Nested(SimpleAddress, required=True)


class User(Schema):
    """
    Schema of a User
    """

    username = fields.Str(required=True)
    age = fields.Int(required=True, min=18, error="Must be over 18 to be a user")
    tags = fields.List(fields.Str())


class StandardResponseSchema(Schema):
    """
    Define Standard Response Schema
    """

    status = fields.Str(required=True)
    message = fields.Str(required=True)


class ErrorDetailSchema(Schema):
    """
    Schema to define the detail of an error
    """

    type = fields.Str(required=True)
    # Todo: allow for lists or string depending on error pylint: disable = fixme
    # message = fields.List(fields.Nested())

    class Meta:
        """ Include unknown fields in the deserialized output """

        unknown = INCLUDE


class ErrorResponseSchema(Schema):
    """
    Schema to define an error response
    """

    success = fields.Str(required=True)
    error = fields.Nested(ErrorDetailSchema)


class StockProductTypeSchema(Schema):
    """

    """

    product_type = fields.Str(
        required=True,
        validate=validate.OneOf(
            [
                "toilet_paper",
                "soap",
                "hand_sanitiser",
                "milk",
                "bread",
                "pasta",
                "tinned_food",
                "fresh_fruit",
                "fresh_vegetables",
            ]
        ),
        description="Product type the report relates to",
    )


class StockItemSchema(StockProductTypeSchema):
    """
    Stock item schema (extends Product Types Schema)
    """

    input_address = fields.Str(
        required=True, description="he raw address searched by the user"
    )
    resolved_address = fields.Str(
        required=True, description="Resolved address from the geocoder"
    )
    geocode = fields.Str(
        required=True, description="Resolved geocode from the geocoder"
    )
    lat = fields.Str(required=True, description="Resolved latitude from the geocoder")
    lng = fields.Str(required=True, description="Resolved longitude from the geocoder")
    stock_level = fields.Int(
        required=True,
        validate=validate.Range(min=0, max=3),
        description="Reported stock level of the product",
    )

    datetime = fields.DateTime(
        required=True,
        description="Time and date of report format='%Y-%m-%dT%H:%M:%Sz' ",
    )  # format='%Y-%m-%dT%H:%M:%Sz'


class StockLevelReportSchema(Schema):
    """
    A submission of the stock level of a specific product type at a specific location
    """

    data = fields.List(fields.Nested(StockItemSchema))
