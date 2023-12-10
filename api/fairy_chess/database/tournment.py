from datetime import datetime

from pydantic import BaseModel, Field, field_validator
from pydantic_mongo import ObjectIdField, AbstractRepository

from fairy_chess.config import HASH_KEY
from fairy_chess.database import database


class TornmentModel(BaseModel):
    id: ObjectIdField = None
    name: str = Field(..., description="Tournment Name")
    starts_at: datetime = Field(..., description="Tornment start date")
    creator_id: str = Field(..., description="User create riot id")


    def __eq__(self, other: 'TornmentModel') -> bool:
        return self.name == other.name


class TornmentRepository(AbstractRepository[TornmentModel]):

    def fetch(self):
        return self.find_by()
    
    def find_by_name(self, name: str):
        return self.find_by({"name", name})

    class Meta:
        collection_name = 'tournment'

tournment_repository = TornmentRepository(database=database)