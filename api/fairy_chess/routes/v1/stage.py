from typing import Annotated

from fastapi import APIRouter, Header

from fairy_chess.controllers.token import decode_token
from fairy_chess.controllers.stage import StageController   

stage_router = APIRouter(prefix="/stage", tags=["admin"])

@stage_router.get('/')
def create(contest_id: str, x_token: Annotated[str, Header()] = None):
    decode_token(x_token)
    return StageController().fetch(contest_id=contest_id)


@stage_router.post('/{stage_id}/start')
def start(stage_id: str, x_token: Annotated[str, Header()] = None):
    user_id = decode_token(x_token)
    return StageController().start(stage_id=stage_id, user_id=user_id)