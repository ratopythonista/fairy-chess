from typing import Annotated

from fastapi import APIRouter, Header

from fairy_chess.controllers.token import decode_token
from fairy_chess.controllers.lobby import LobbyController   

lobby_router = APIRouter(prefix="/lobby", tags=["admin"])

@lobby_router.get('/{stage_id}')
def fetch_by_stage(stage_id: str, x_token: Annotated[str, Header()] = None):
    decode_token(x_token)
    return LobbyController().fetch(stage_id=stage_id)