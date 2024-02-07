from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from fairy_chess.pages import include_routes


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

include_routes(app)