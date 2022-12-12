from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

def templates_config(app: FastAPI):
    app.mount("/static", StaticFiles(directory="./static"), name="static")

    return Jinja2Templates(directory="./templates")