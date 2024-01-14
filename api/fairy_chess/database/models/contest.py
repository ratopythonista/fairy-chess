from uuid import uuid4

from typing import Optional
from sqlmodel import Field, SQLModel, select

from fairy_chess.database.models.user import User


class Contest(SQLModel, table=True):
    id: Optional[str] = Field(default=str(uuid4()), primary_key=True)
    title: str = Field(index=True, nullable=False, unique=True)
    timestamp: float = Field(nullable=False)
    size: int = Field(nullable=False)

    creator: Optional[str] = Field(nullable=False, foreign_key="user.id")


class ContestUser(SQLModel, table=True):
    contest_id: str = Field(nullable=False, primary_key=True, foreign_key="contest.id")
    user_id: str = Field(nullable=False, primary_key=True, foreign_key="user.id")
    check_in: Optional[bool] = Field(default=False, primary_key=True)


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
    
    @staticmethod
    def competitors(contest_id: str, check_in: bool | None = None):
        query = select(User).join(ContestUser).where(ContestUser.contest_id == contest_id)
        if check_in:
            return query.where(ContestUser.check_in == True)
        return query
    
    @staticmethod
    def find_registred(contest_id: str, user_id: str):
        return select(ContestUser).where(
            ContestUser.contest_id == contest_id, ContestUser.user_id == user_id
        )
