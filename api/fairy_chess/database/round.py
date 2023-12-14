from bson import ObjectId

from pydantic import BaseModel, Field, field_validator
from pydantic_mongo import ObjectIdField, AbstractRepository

from fairy_chess.database import database

class RoundClassificationModel(BaseModel):
    riot_id: str = Field(..., description="Participant Id")
    points: int = Field(0, description="Round points")

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
        return self.name == other.name


class RoundRepository(AbstractRepository[RoundModel]):

    def find_by_tournment(self, tournment_id: str) -> list[RoundModel]:
        return self.find_by({"tournment_id": tournment_id})
    
    def find_one(self, round: RoundModel) -> RoundModel:
        return self.find_one_by({"name": round.name, "tournment_id": round.tournment_id})
    
    def find_one_by_id(self, round_id) -> RoundModel | None:
        return super().find_one_by_id(ObjectId(round_id))
    
    def find_previous(self, round: RoundModel) -> RoundModel:
        round_base = self.find_one_by({"tournment_id": round.tournment_id, "order": round.tournment_id-1})
        competitors = sorted(round_base.competitors, lambda x: x.points)[:round.qty_advance]
        

    class Meta:
        collection_name = 'round'

round_repository = RoundRepository(database=database)