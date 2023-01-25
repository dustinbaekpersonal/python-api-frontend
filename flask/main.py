"""
Main file for the template application
"""
from app import create_app

# Initialise Flask App object
app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0")
