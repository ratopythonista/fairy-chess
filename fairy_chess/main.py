import uptrace
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, Depends, Header, Request
from starlette_context import context, request_cycle_context
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

from data.lobby import get_lobby
from data.match import get_matches
from data.tournament import get_tournament, get_tournament_list


async def my_context_dependency(request: Request, x_client_id = Header(None)):
    data = {"x_client_id": x_client_id, "request": request}
    with request_cycle_context(data):
        yield


app = FastAPI(dependencies=[Depends(my_context_dependency)])

app.mount("/static", StaticFiles(directory="./static"), name="static")

uptrace.configure_opentelemetry(
    service_name="fairy_chess",
    service_version="0.1.0",
)
FastAPIInstrumentor.instrument_app(app)

templates = Jinja2Templates(directory="./templates")


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