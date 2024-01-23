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

@stage_router.post('/{stage_id}/matches/{round}')
def start(stage_id: str, round: int, x_token: Annotated[str, Header()] = None):
    user_id = decode_token(x_token)
    return StageController().matches(stage_id=stage_id, round=round, user_id=user_id)

@stage_router.post('/{stage_id}')
def update(
        stage_id: str, 
        start_players: int = None,
        qtd_rounds: int = None,
        shuffle_rate: int = None,
        x_token: Annotated[str, Header()] = None
    ):
    user_id = decode_token(x_token)
    return StageController().update(user_id=user_id, stage_id=stage_id, start_players=start_players, qtd_rounds=qtd_rounds, shuffle_rate=shuffle_rate)