from typing import Annotated
from datetime import datetime

from pydantic import BaseModel, Field
from fastapi import APIRouter, Body, Header, Query, Path

from fairy_chess.controllers.token import Token
from fairy_chess.controllers.lobby import LobbyController  

lobby_router = APIRouter(prefix="/lobby", tags=["admin"])


class LobbyCreateRequest(BaseModel):
    name: str = Field(..., description="Lobby Name")
    round_id: str = Field(..., description="Tournment that lobby belongs")


@lobby_router.post('/create')
def create(
    x_token: Annotated[str, Header()] = None,
    lobby: Annotated[LobbyCreateRequest, Body(..., description="Lobby Creation Request")] = None 
):
    return LobbyController(Token.decode(x_token), lobby).create()


@lobby_router.get('/')
def fetch(round_id: Annotated[str, Query()], x_token: Annotated[str, Header()] = None,):
    return LobbyController(Token.decode(x_token)).fetch(round_id)
