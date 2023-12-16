from typing import Annotated
from datetime import datetime

from pydantic import BaseModel, Field
from fastapi import APIRouter, Body, Header, Query, Path

from fairy_chess.controllers.token import Token
from fairy_chess.controllers.round import RoundController  

round_router = APIRouter(prefix="/round", tags=["admin"])


class RoundRegisterRequest(BaseModel):
    name: str = Field(..., description="Round Name")
    order: int = Field(..., description="Round order in tournment")
    qty_advance: int = Field(..., description="Players that advance to next round")
    tournment_id: str = Field(..., description="Tournment that round belongs")


@round_router.post('/create')
def create(
    x_token: Annotated[str, Header()] = None,
    round: Annotated[RoundRegisterRequest, Body(..., description="Round Creation Request")] = None 
):
    return RoundController(Token.decode(x_token), round).create()


@round_router.get('/')
def fetch(tournment_id: Annotated[str, Query()], x_token: Annotated[str, Header()] = None,):
    return RoundController(Token.decode(x_token)).fetch(tournment_id)

@round_router.post('/start/{round_id}')
def fetch(round_id: Annotated[str, Path()], x_token: Annotated[str, Header()] = None,):
    return RoundController(Token.decode(x_token)).start(round_id)