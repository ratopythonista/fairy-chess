from bson import ObjectId
from collections import Counter

from pydantic import BaseModel, Field, field_validator, computed_field
from pydantic_mongo import ObjectIdField, AbstractRepository

from fairy_chess.database import database

class RoundClassificationModel(BaseModel):
    riot_id: str = Field(..., description="Participant Id")
    placement: list[int] = Field([], description="Round placements")

    @computed_field(description="Round Points")
    @property
    def points(self) -> int:
        return sum([9-place for place in self.placement])
    
    def __gt__(self, other: 'RoundClassificationModel'):
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

class RoundModel(BaseModel):
    id: ObjectIdField = None
    name: str = Field(..., description="Round Name")
    order: int = Field(..., description="Round order in tournment")
    qty_advance: int = Field(..., description="Players that advance to next round")
    tournment_id: ObjectIdField | str = Field(..., description="Tournment that round belongs")
    competitors: list[RoundClassificationModel] = Field([], description="Round Competitors")

    @field_validator("tournment_id")
    @classmethod
    def tournment_id_validator(cls, tournment_id: str):
        return ObjectIdField(tournment_id)
    

    def __eq__(self, other: 'RoundModel') -> bool:
        return self.name == other.name and self.tournment_id == other.tournment_id


class RoundRepository(AbstractRepository[RoundModel]):

    def find_by_tournment(self, tournment_id: str) -> list[RoundModel]:
        return self.find_by({"tournment_id": tournment_id})
    
    def find_one(self, round: RoundModel) -> RoundModel:
        return self.find_one_by({"name": round.name, "tournment_id": round.tournment_id})
    
    def find_one_by_id(self, round_id) -> RoundModel | None:
        return super().find_one_by_id(ObjectId(round_id))
    
    def find_previous(self, round: RoundModel) -> RoundModel:
        previous_round = self.find_one_by({"tournment_id": round.tournment_id, "order": round.order-1})
        return sorted(
            [competitor for competitor in previous_round.competitors], reverse=True
        )[:previous_round.qty_advance]

    class Meta:
        collection_name = 'round'

round_repository = RoundRepository(database=database)