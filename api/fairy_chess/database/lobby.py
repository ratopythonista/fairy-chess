from bson import ObjectId
from collections import Counter

from pydantic import BaseModel, Field, field_validator, computed_field
from pydantic_mongo import ObjectIdField, AbstractRepository

from fairy_chess.database import database

class LobbyClassificationModel(BaseModel):
    riot_id: str = Field(..., description="Participant Id")
    placement: list[int] = Field([], description="Lobby placements")

    @computed_field(description="Lobby Points")
    @property
    def points(self) -> int:
        return sum([9-place for place in self.placement])
    
    def __gt__(self, other: 'LobbyClassificationModel'):
        self_placement_count = Counter(self.placement)
        other_placement_count = Counter(other.placement)
        if self.points > other.points:
            return True
        elif self.points == other.points:
            place = 1
            while self_placement_count.get(place, 0) == other_placement_count.get(place, 0):
                place += 1
                if place == 9:
                    break
            return self_placement_count.get(place, 0) > other_placement_count.get(place, 0)

class LobbyModel(BaseModel):
    id: ObjectIdField = None
    name: str = Field(..., description="Lobby Name")
    is_done: bool = Field(False, description="Set if lobby matches is done")
    round_id: ObjectIdField | str = Field(..., description="Round that lobby belongs")
    competitors: list[LobbyClassificationModel] = Field([], description="Lobby Competitors")

    @field_validator("round_id")
    @classmethod
    def round_id_validator(cls, round_id: str):
        return ObjectIdField(round_id)

    def __eq__(self, other: 'LobbyModel') -> bool:
        return self.name == other.name and self.round_id == other.round_id


class LobbyRepository(AbstractRepository[LobbyModel]):

    def find_by_round(self, round_id: str) -> list[LobbyModel]:
        return self.find_by({"round_id": round_id})
    
    def find_one(self, lobby: LobbyModel) -> LobbyModel:
        return self.find_one_by({"name": lobby.name, "round_id": lobby.round_id})
    
    def find_one_by_id(self, round_id) -> LobbyModel | None:
        return super().find_one_by_id(ObjectId(round_id))

    class Meta:
        collection_name = 'lobby'

lobby_repository = LobbyRepository(database=database)