# pylint: disable=too-few-public-methods
"""
Define Flask App configuration settings for each environment
"""
import os


def get_db_connection_string() -> str:
    """
    Get DB connection string from env vars

    In future this function can be altered for vault secrets etc.
    """
    db_host = os.getenv("POSTGRES_HOST_URI", None)
    db_user = os.getenv("POSTGRES_DB_USER", None)
    db_password = os.getenv("POSTGRES_DB_PASSWORD", None)
    db_name = os.getenv("POSTGRES_DB_NAME", None)
    db_port = os.getenv("POSTGRES_PORT", None)

    engine_url = "postgresql://{}:{}@{}:{}/{}".format(
        db_user, db_password, db_host, db_port, db_name
    )

    if str(None) in engine_url:
        # raise app initialisation error if the engine_url is incomplete
        pass

    return engine_url


class BaseConfig:
    """
    Base Class to define th configurations of the Flask app
    """

    API_PREFIX = "/api"
    TESTING = False
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SWAGGER = {
        "title": "Template Flask Open API Documentation ",
        "uiversion": 3,
        "specs_route": "/swagger/",
    }
    SQLALCHEMY_DATABASE_URI = get_db_connection_string()


class DevConfig(BaseConfig):
    """
    Development environment configurations of the Flask app
    """

    FLASK_ENV = "development"
    DEBUG = True


class ProductionConfig(BaseConfig):
    """
    Production environment configurations of the Flask app
    """

    FLASK_ENV = "production"


class TestConfig(BaseConfig):
    """
    Test environment configurations of the Flask app
    """

    FLASK_ENV = "development"
    TESTING = True
    DEBUG = True


# class DbConfig:
#     DB_FILEPATH = "stock_db.csv"

DbConfig = dict(DB_FILEPATH=os.getenv("CSV_FILE", "flask/db/stock_db.csv"))
