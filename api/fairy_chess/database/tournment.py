from datetime import datetime

from pydantic import BaseModel, Field
from pydantic_mongo import ObjectIdField, AbstractRepository

from fairy_chess.database import database

class TourmentClassificationModel(BaseModel):
    riot_id: str = Field(..., description="Participant Id")
    points: int = Field(0, description="Tournment points")

class TournmentModel(BaseModel):
    id: ObjectIdField = None
    name: str = Field(..., description="Tournment Name")
    starts_at: float = Field(..., description="Tournment start date")
    creator_id: str = Field('', description="User create riot id")
    competitors: list[TourmentClassificationModel] = Field('', description="Tourment Competitors")

    def __eq__(self, other: 'TournmentModel') -> bool:
        return self.name == other.name


class TournmentRepository(AbstractRepository[TournmentModel]):

    def fetch(self) -> list[TournmentModel]:
        return self.find_by({})
    
    def find_by_name(self, name: str) -> TournmentModel:
        return self.find_one_by({"name": name})

    class Meta:
        collection_name = 'tournment'

tournment_repository = TournmentRepository(database=database)