from typing import Annotated

from fastapi import APIRouter, Body, Header

from fairy_chess.controllers.token import decode_token
from fairy_chess.controllers.contest import ContestController   

contest_router = APIRouter(prefix="/contest", tags=["admin"])

@contest_router.post('/create')
def create(
    title: Annotated[str, Body()], 
    timestamp: Annotated[float, Body()],
    size: Annotated[int, Body()],
    x_token: Annotated[str, Header()] = None
):
    user_id = decode_token(x_token)
    return ContestController().create(title=title, timestamp=timestamp, size=size, user_id=user_id)


@contest_router.get('/')
def fetch(all: bool = False, x_token: Annotated[str, Header()] = None):
    user_id = decode_token(x_token)
    return ContestController().fetch(user_id=None if all else user_id)


# @contest_router.post('/register/{tournment_id}')
# def register(tournment_id: str, x_token: Annotated[str, Header()] = None,):
#     jwt: JWT = Token.decode(x_token)
#     return TournmentController.register(tournment_id, jwt.puuid)