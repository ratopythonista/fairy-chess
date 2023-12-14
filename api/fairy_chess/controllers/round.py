from pydantic import BaseModel
from fastapi import HTTPException

from fairy_chess.controllers.token import Token
from fairy_chess.controllers.tournment import TournmentModel, tournment_repository
from fairy_chess.database.round import (
    RoundModel, round_repository, RoundClassificationModel
)


class RoundController:
    def __init__(self, token: Token, round: BaseModel = None) -> None:
        if round:
            self.round: RoundModel = RoundModel(**round.model_dump())
        self.token = token

    def create(self):
        round_base = round_repository.find_one(self.round)
        if not round_base:
            round_repository.save(self.round)
            return self.round.model_dump()
        raise HTTPException(status_code=403, detail="Round alredy exists")

    def fetch(self, tournment_id: str) -> list[dict]:
        return [round.model_dump() for round in round_repository.find_by_tournment(tournment_id)]


    def start(self, round_id: str):
        round_base = round_repository.find_one_by_id(round_id)
        if round_base.order == 1:
            tournment = tournment_repository.find_one_by_id(round_base.tournment_id)
            round_base.competitors = tournment.competitors
        else
            round_base.competitors = round_repository.find_previous(round_base).competitors[:4]