import random as rd

from pydantic import BaseModel
from fastapi import HTTPException

from fairy_chess.controllers.token import Token
from fairy_chess.controllers.round import round_repository
from fairy_chess.database.lobby import (
    LobbyModel, lobby_repository, LobbyClassificationModel
)


class LobbyController:
    def __init__(self, token: Token, lobby: BaseModel = None) -> None:
        if lobby:
            self.lobby: LobbyModel = LobbyModel(**lobby.model_dump())
        self.token = token

    def create(self):
        if not lobby_repository.find_one(self.lobby):
            round_base = round_repository.find_one_by_id(self.lobby.round_id)
            if round_base:
                allocated_competitors = set()
                all_competitors = {competitor.riot_id for competitor in round_base.competitors}
                for base_lobby in lobby_repository.find_by_round(self.lobby.round_id):
                    for competitor in base_lobby.competitors:
                        allocated_competitors.add(competitor.riot_id)
                aviable_competitors = allocated_competitors ^ all_competitors
                if aviable_competitors:
                    self.lobby.competitors = [
                        LobbyClassificationModel(riot_id=competitor) 
                        for competitor in rd.sample(list(aviable_competitors), k=8)
                    ]
                    lobby_repository.save(self.lobby)
                    return self.lobby.model_dump()
                raise HTTPException(status_code=404, detail="There is no more aviable players for this round")
            raise HTTPException(status_code=404, detail="Round does not exists")
        raise HTTPException(status_code=403, detail="Lobby alredy exists")

    def fetch(self, round_id: str) -> list[dict]:
        return [lobby.model_dump() for lobby in lobby_repository.find_by_round(round_id)]
