from fastapi.responses import HTMLResponse

from fastapi import FastAPI, Depends
from starlette_context import context


from data.lobby import get_lobby
from data.match import get_matches
from data.tournament import get_tournament, get_tournament_list

from utils.contex import context_config
from utils.tracing import tracing_config
from utils.templates import templates_config

app = FastAPI(dependencies=[Depends(context_config)])


tracing_config(app)
templates = templates_config(app)


@app.get("/", response_class=HTMLResponse)
async def index():
    context["info"] = get_tournament_list()
    return templates.TemplateResponse("index.html", context.data)

@app.get("/lobby", response_class=HTMLResponse)
async def lobby():
    context.data["info"] = get_lobby() 
    return templates.TemplateResponse("lobby.html", context.data)

@app.get("/match", response_class=HTMLResponse)
async def match():
    context.data["info"] = get_matches() 
    return templates.TemplateResponse("match.html", context.data)

@app.get("/tournament", response_class=HTMLResponse)
async def tournament():
    context.data["info"] = get_tournament() 
    return templates.TemplateResponse("tournament.html", context.data)
