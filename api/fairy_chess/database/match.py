from bson import ObjectId
from collections import Counter

from pydantic import BaseModel, Field, field_validator, computed_field
from pydantic_mongo import ObjectIdField, AbstractRepository

from fairy_chess.database import database

class MatchClassificationModel(BaseModel):
    riot_id: str = Field(..., description="Participant Id")
    placement: int = Field(..., description="Match placement")


class MatchModel(BaseModel):
    id: ObjectIdField = None
    riot_match_id: str = Field(..., description="Riot Match Identifier")
    lobby_id: ObjectIdField | str = Field(..., description="Lobby that match belongs")
    competitors: list[MatchClassificationModel] = Field([], description="Match Competitors")

    @field_validator("lobby_id")
    @classmethod
    def lobby_id_validator(cls, lobby_id: str):
        return ObjectIdField(lobby_id)

    def __eq__(self, other: 'MatchModel') -> bool:
        return self.riot_match_id == other.riot_match_id


class MatchRepository(AbstractRepository[MatchModel]):

    def find_by_lobby(self, lobby_id: str) -> list[MatchModel]:
        return self.find_by({"lobby_id": lobby_id})
    
    def find_one(self, match: MatchModel) -> MatchModel:
        return self.find_one_by({"riot_match_id": match.riot_match_id})

    class Meta:
        collection_name = 'match'

match_repository = MatchRepository(database=database)