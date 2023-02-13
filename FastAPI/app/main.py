"""
Main file for the template application
"""
from fastapi import FastAPI
from routers import items
import uvicorn


# Initialise FastAPI App object
app = FastAPI(title = "Stock Level API")

app.include_router(items.router)

@app.get("/")
async def root():
     return {"message": "Welcom to FastAPI Course!"}

if __name__ == "__main__":
     uvicorn.run(app, host="0.0.0.0", port=8000)
     # print("main file")