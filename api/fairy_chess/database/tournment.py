from bson import ObjectId

from pydantic import BaseModel, Field
from pydantic_mongo import ObjectIdField, AbstractRepository

from fairy_chess.database import database


class Match(BaseModel):
    name: str = Field(..., description="Match Name")
    competitors: list[str] = Field(..., description="")
    placement: list[int] = Field(..., description="")
    stage: str = Field(..., description="Stage name")


class Stage(BaseModel):
    name: str = Field(..., description="Stage name")
    competitors: list[str] = Field(..., description="")
    pontuation: list[int] = Field(..., description="")
    matches: list[Match] = Field([], description="Tourment Stages")


class TournmentModel(BaseModel):
    id: ObjectIdField = None
    name: str = Field(..., description="Tournment Name")
    starts_at: float = Field(..., description="Tournment start date")
    creator_id: str = Field(..., description="User create riot id")
    stages: list[Stage] = Field([], description="Tourment Stages")

    def __eq__(self, other: 'TournmentModel') -> bool:
        return self.name == other.name


class TournmentRepository(AbstractRepository[TournmentModel]):

    def fetch(self) -> list[TournmentModel]:
        return self.find_by({})
    
    def find_by_name(self, name: str) -> TournmentModel:
        return self.find_one_by({"name": name})
    
    def find_one_by_id(self, tournemt_id) -> TournmentModel | None:
        return super().find_one_by_id(ObjectId(tournemt_id))

    class Meta:
        collection_name = 'tournment'

tournment_repository = TournmentRepository(database=database)