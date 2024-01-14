from uuid import uuid4

from typing import Optional
from sqlmodel import Field, SQLModel, select


class Contest(SQLModel, table=True):
    id: Optional[str] = Field(default=str(uuid4()), primary_key=True)
    title: str = Field(index=True, nullable=False, unique=True)
    timestamp: float = Field(nullable=False)
    size: int = Field(nullable=False)

    creator: Optional[str] = Field(nullable=True, foreign_key="user.id")


class ContestQuery:
    @staticmethod
    def find_all(user_id: str = None):
        query = select(Contest)
        if user_id:
            return query.where(Contest.creator == user_id)
        return query
    
    @staticmethod
    def find_by_id(contest_id: str):
        return select(Contest).where(Contest.id == contest_id)
