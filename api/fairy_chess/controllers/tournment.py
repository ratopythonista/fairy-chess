from pydantic import BaseModel
from fastapi import HTTPException

from fairy_chess.controllers.token import Token
from fairy_chess.database.tournment import TournmentModel, tournment_repository


class TournmentController:
    def __init__(self, token: Token, tournment: BaseModel = None) -> None:
        if tournment:
            self.tournment: TournmentModel = TournmentModel(**tournment.model_dump())
        self.token = token

    def create(self):
        tournment_base = tournment_repository.find_by_name(self.tournment.name)
        from loguru import logger
        logger.debug(tournment_base)
        if not tournment_base:
            self.tournment.creator_id = self.token.riot_id
            tournment_repository.save(self.tournment)
            return self.tournment.model_dump()
        raise HTTPException(status_code=403, detail="Tournemt alredy exists")

    def fetch(self) -> list[dict]:
        return [tournment.model_dump() for tournment in tournment_repository.fetch()]

    def register(self, tournment_id: str):
        tournment_base = tournment_repository.find_one_by_id(tournment_id)
        if tournment_base:
            self.tournment.competitors.append(
                {"riot_id": self.token.riot_id, "points": 0}
            )
