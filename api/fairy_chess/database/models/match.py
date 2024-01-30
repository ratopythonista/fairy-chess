from uuid import uuid4

from typing import Optional
from sqlmodel import Field, SQLModel, select

from fairy_chess.database.models.user import User
from fairy_chess.database.models.stage import Stage

class Match(SQLModel, table=True):
    id: Optional[str] = Field(default=str(uuid4()), primary_key=True)
    title: str = Field(index=True, nullable=False, unique=False)
    is_sync: bool = Field(default=False, nullable=False)
    riot_id: str = Field(nullable=True)

    stage_id: Optional[str] = Field(nullable=False, foreign_key="stage.id")


class MatchUser(SQLModel, table=True):
    match_id: str = Field(nullable=False, primary_key=True, foreign_key="match.id")
    user_id: str = Field(nullable=False, primary_key=True, foreign_key="user.id")
    placement: Optional[bool] = Field(default=False, primary_key=True)


class MatchQuery:
    @staticmethod
    def find_by_id(match_id: str):
        return select(Match).where(Match.id == match_id)
    
    @staticmethod
    def find_stage_matches(stage_id: str):
        return select(Match).where(Match.stage_id == stage_id)