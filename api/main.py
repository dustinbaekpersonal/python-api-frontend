"""Main file for the template application."""
import items
import uvicorn
from fastapi import FastAPI

app = FastAPI(title="Stock Level API")

app.include_router(items.router)


@app.get("/")
async def root():
    """Root api endpoint."""
    return {"message": "Welcome to FastAPI Course!"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
