"""Main file for the template application."""
from fastapi import FastAPI

from backend.items import router

app = FastAPI(title="Stock Level API")

app.include_router(router)


@app.get("/")
async def root():
    """Root api endpoint."""
    return {"message": "Welcome to FastAPI Course!"}
