from uuid import uuid4

from typing import Optional
from sqlmodel import Field, SQLModel, select

from fairy_chess.database import BaseRepository
from fairy_chess.database.models.user import User
from fairy_chess.database.models.contest import Contest


class Stage(SQLModel, table=True):
    id: Optional[str] = Field(default=str(uuid4()), primary_key=True)
    title: str = Field(index=True, nullable=False, unique=False)
    start_players: int = Field(nullable=False)
    contest_id: str = Field(nullable=False, primary_key=True, foreign_key="contest.id")


class StageUser(SQLModel, table=True):
    stage_id: str = Field(nullable=False, primary_key=True, foreign_key="stage.id")
    user_id: str = Field(nullable=False, primary_key=True, foreign_key="user.id")
    check_in: Optional[bool] = Field(default=False, primary_key=True)


class StageRepository(BaseRepository):

    @staticmethod
    def fetch(contest_id: str):
        return select(Stage).where(Stage.contest_id == contest_id)
    
    @staticmethod
    def find_by_id(stage_id: str):
        return select(Stage).where(Stage.id == stage_id)
    
    @staticmethod
    def find_by_start_players(start_players: int):
        return select(Stage).where(Stage.start_players == start_players)

    @staticmethod
    def get_users(stage_id: str):
        return select(StageUser).where(StageUser.stage_id == stage_id)
