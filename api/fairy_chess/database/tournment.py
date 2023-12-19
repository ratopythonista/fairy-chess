from bson import ObjectId

from pydantic import BaseModel, Field
from pydantic_mongo import ObjectIdField, AbstractRepository

from fairy_chess.database import database  
from fairy_chess.services.riot import Match


class Lobby(BaseModel):
    name: str = Field(..., description="")
    competitors: list[str] = Field(..., description="")
    total_matches: int = Field(..., description="Quantity of matches")
    matches: list[Match] = Field([], description="Matches for this lobby")


class Round(BaseModel):
    name: str = Field(..., description="Round name")
    qty_advance: int = Field(..., description="Players that advence to next round")
    competitors: list[str] = Field(..., description="")
    lobbys: list[Lobby] = Field(..., description="Lobbys for this round")


class TournmentModel(BaseModel):
    id: ObjectIdField = None
    name: str = Field(..., description="Tournment Name")
    starts_at: float = Field(..., description="Tournment start date")
    creator_id: str = Field(..., description="User create riot id")
    competitors: list[str] = Field([], description="Tourment Competitors")
    rounds: list[Round] = Field([], description="Tourment Competitors")

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