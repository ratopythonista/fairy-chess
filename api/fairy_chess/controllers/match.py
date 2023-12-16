import random as rd

from pydantic import BaseModel
from fastapi import HTTPException

from fairy_chess.services.riot import Riot
from fairy_chess.controllers.token import Token
from fairy_chess.controllers.round import round_repository
from fairy_chess.database.match import (
    MatchModel, match_repository, MatchClassificationModel
)


class MatchController:
    def __init__(self, token: Token, lobby_id: str) -> None:
        self.token = token
        self.lobby_id = lobby_id

    def create(self):
        riot = Riot(self.token.riot_id)
        match = MatchModel(riot_match_id=riot.match, lobby_id=self.lobby_id)
        for riot_id, placement in riot.placement:
            match.competitors.append(
                MatchClassificationModel(
                    riot_id=riot_id,
                    placement=placement
                )
            )
        match_repository.save(match)
        return match.model_dump()

    def fetch(self) -> list[dict]:
        return [match.model_dump() for match in match_repository.find_by_lobby(self.lobby_id)]
