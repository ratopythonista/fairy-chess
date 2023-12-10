from fastapi import HTTPException

from fairy_chess.controllers.token import Token
from fairy_chess.database.tournment import TornmentModel, tournment_repository


class TornmentController:
    def __init__(self, tournment: TornmentModel, token: Token) -> None:
        self.tournment: TornmentModel = tournment
        self.token = token

    def create(self):
        tournment_base = tournment_repository.find_by_name(self.tournment.name)
        if not tournment_base:
            self.tournment.creator_id = self.token.riot_id
            return tournment_repository.save(self.tournment)
        raise HTTPException(status_code=403, detail="Tornment alredy exists")

    def fetch(self):
        return tournment_repository.fetch()
