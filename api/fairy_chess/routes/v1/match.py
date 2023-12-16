from typing import Annotated

from fastapi import APIRouter, Header, Query, Path

from fairy_chess.controllers.token import Token
from fairy_chess.controllers.match import MatchController  

match_router = APIRouter(prefix="/match", tags=["admin"])


@match_router.post('/sync/{lobby_id}')
def create(
    lobby_id: Annotated[str, Path(..., description="Lobby for this Match")],
    x_token: Annotated[str, Header()] = None
):
    return MatchController(Token.decode(x_token), lobby_id).create()


@match_router.get('/')
def fetch(lobby_id: Annotated[str, Query()], x_token: Annotated[str, Header()] = None,):
    return MatchController(Token.decode(x_token), lobby_id).fetch()
