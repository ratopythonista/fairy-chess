from typing import Annotated

from fastapi import APIRouter, Header

from fairy_chess.controllers.token import decode_token
from fairy_chess.controllers.lobby import LobbyController   

lobby_router = APIRouter(prefix="/lobby", tags=["admin"])

@lobby_router.get('/{stage_id}')
def fetch_by_stage(stage_id: str, x_token: Annotated[str, Header()] = None):
    decode_token(x_token)
    return LobbyController().fetch(stage_id=stage_id)


@lobby_router.post('/{lobby_id}/match/{match_index}')
def create_match(lobby_id: str, match_index: int, x_token: Annotated[str, Header()] = None):
    user_id = decode_token(x_token)
    return LobbyController().create_match(lobby_id=lobby_id, match_index=match_index, user_id=user_id)