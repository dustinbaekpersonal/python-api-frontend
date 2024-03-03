"""Define database connection."""
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Load environment variables from .env file
load_dotenv()

# Get database credentials from environment variables
user_name = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
db_name = os.getenv("DB_NAME")

URL_DATABASE = f"postgresql://{user_name}:{password}@localhost:5432/{db_name}"

engine = create_engine(URL_DATABASE)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
