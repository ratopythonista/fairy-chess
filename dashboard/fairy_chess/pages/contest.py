from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
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

@contest_router.post("/{contest_id}/register")
async def register_contest(request: Request, contest_id: str):
    Contest().register(contest_id, request.client.host)
    return RedirectResponse(url=f"/contest/{contest_id}", status_code=302)

@contest_router.get("/{contest_id}")
async def contest_detail(request: Request, contest_id: str):
    user = User().login("teste@fc.com", "12345678", request.client.host) # ONLY FOR TESTING PURPOSES
    
    contest = Contest().fetch_by_id(contest_id, request.client.host)


    return templates.TemplateResponse(
        name="contest_detail.html", context={"request": request, "contest_detail": contest, "title": f"Contest {contest.get('title')}", "user": user}
    )
