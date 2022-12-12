from uuid import uuid4, UUID

from loguru import logger
from dotenv import load_dotenv
from fastapi import HTTPException, Request
from starlette_context import context
from fastapi.responses import HTMLResponse
from starlette.status import HTTP_303_SEE_OTHER
from starlette.responses import RedirectResponse
from fastapi import FastAPI, Depends, Form, Response

import fairy_chess.data.user as user_data
import fairy_chess.data.session as session_data

from fairy_chess.data.lobby import get_lobby
from fairy_chess.data.match import get_matches
from fairy_chess.data.tournament import get_tournament, get_tournament_list

from fairy_chess.utils.contex import context_config
from fairy_chess.utils.tracing import tracing_config
from fairy_chess.utils.templates import templates_config

app = FastAPI(dependencies=[Depends(context_config)])

load_dotenv()
tracing_config(app)
templates = templates_config(app)


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    context["info"] = get_tournament_list()
    context["user"] = session_data.get_current(request.client.host)
    return RedirectResponse(url='/match', status_code=HTTP_303_SEE_OTHER)

@app.get("/match", response_class=HTMLResponse)
async def match(request: Request):
    context["info"] = get_matches() 
    context["user"] = session_data.get_current(request.client.host)
    return templates.TemplateResponse("match.html", context.data)

@app.get("/login", response_class=HTMLResponse)
async def login():  
    return templates.TemplateResponse("login.html", context.data)

@app.get("/register", response_class=HTMLResponse)
async def register():  
    return templates.TemplateResponse("register.html", context.data)

@app.get("/todo", response_class=HTMLResponse)
async def todo():  
    return templates.TemplateResponse("todo.html", context.data)

@app.post("/auth", response_class=HTMLResponse)
async def auth(request: Request, username: str = Form(), password: str = Form()):
    user_id = user_data.authenticate(email=username, password=password)
    session_data.login(request.client.host, user_id)
    return RedirectResponse(url='/', status_code=HTTP_303_SEE_OTHER)

@app.post("/users", response_class=HTMLResponse)
async def create_user(username: str = Form(), password: str = Form(), name: str = Form()):
    user_data.put(email=username, password=password, name=name)
    return RedirectResponse(url='/login', status_code=HTTP_303_SEE_OTHER)

@app.get("/logout", response_class=HTMLResponse)
async def logout(request: Request):
    session_data.logout(request.client.host)
    return RedirectResponse(url='/', status_code=HTTP_303_SEE_OTHER)