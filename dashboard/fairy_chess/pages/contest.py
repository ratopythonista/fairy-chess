from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from fairy_chess.services.fairy_chess_api import User, Contest


templates = Jinja2Templates(directory="templates")
contest_router = APIRouter(prefix="/contest")


@contest_router.get("/", response_class=HTMLResponse)
async def contest(request: Request):
    user = User().login("teste@fc.com", "12345678", request.client.host) # ONLY FOR TESTING PURPOSES

    contest_list = Contest().fetch(request.client.host)

    return templates.TemplateResponse(
        name="contests.html", context={"request": request, "contest_list": contest_list, "title": "Contests", "user": user}
    )