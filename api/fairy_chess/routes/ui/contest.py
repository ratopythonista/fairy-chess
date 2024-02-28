from __future__ import annotations as _annotations

from typing import Annotated

from fastui import components as c
from fastapi import APIRouter, Depends
from fastui import AnyComponent, FastUI
from fastui.events import BackEvent, GoToEvent
from fastui.components.display import DisplayLookup

from fairy_chess.routes.ui.page import FairyChessPage
from fairy_chess.controllers.user import UserController, User
from fairy_chess.controllers.contest import ContestController, Contest


contest_router = APIRouter(prefix="/contest", tags=["ui"])


@contest_router.get('/', response_model=FastUI, response_model_exclude_none=True)
async def profile(
    user: Annotated[User, Depends(UserController.get_from_token)],
    page: int = 1
) -> list[AnyComponent]:
    contest_list = ContestController().fetch()
    page_size = 50
    return FairyChessPage(
        c.Table(
            data=contest_list[(page - 1) * page_size : page * page_size],
            data_model=Contest,
            columns=[
                DisplayLookup(field='title',on_click=GoToEvent(url='/ui/contest/{id}'), table_width_percent=33),
                DisplayLookup(field='start_players', title="Start Players", table_width_percent=33),
                DisplayLookup(field='timestamp', title="Start Time", table_width_percent=33),
            ],
        ),
        c.Pagination(page=page, page_size=page_size, total=len(contest_list)),
        title='Contest',
        user_riot_id=user.riot_id,
    ).render()