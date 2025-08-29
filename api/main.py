from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

from api.h2h_routes import router as h2h_router

app = FastAPI()

# Include head-to-head routes under /h2h
app.include_router(h2h_router)

@app.get("/")
def root():
    return {"message": "Bracket Maker API is running"}
