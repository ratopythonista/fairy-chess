from typing import Annotated

from fastapi import APIRouter, Header

from fairy_chess.controllers.token import decode_token
from fairy_chess.controllers.stage import StageController   

stage_router = APIRouter(prefix="/stage", tags=["admin"])

@stage_router.post('/')
def create(contest_id: str, x_token: Annotated[str, Header()] = None):
    decode_token(x_token)
    return StageController().fetch(contest_id=contest_id)

