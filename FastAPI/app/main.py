"""
Main file for the template application
"""
from fastapi import FastAPI
import items
import uvicorn


# Initialise FastAPI App object
app = FastAPI(title = "Stock Level API")

app.include_router(items.router)

@app.get("/")
async def root():
     return {"message": "Welcome to FastAPI Course!"}

if __name__ == "__main__":
     uvicorn.run(app, host="127.0.0.1", port=8000)
