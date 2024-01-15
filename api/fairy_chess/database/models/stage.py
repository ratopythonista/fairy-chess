from uuid import uuid4

from typing import Optional
from sqlmodel import Field, SQLModel, select

from fairy_chess.database.models.user import User
from fairy_chess.database.models.contest import Contest


class Stage(SQLModel, table=True):
    id: Optional[str] = Field(default=str(uuid4()), primary_key=True)
    title: str = Field(index=True, nullable=False, unique=True)
    start_players: int = Field(nullable=False)
    qtd_rounds: int = Field(nullable=False)
    shuffle_rate: int = Field(nullable=False)


class ContestStages(SQLModel, table=True):
    contest_id: str = Field(nullable=False, primary_key=True, foreign_key="contest.id")
    stage_id: str = Field(nullable=False, primary_key=True, foreign_key="stage.id")


class StageUsers(SQLModel, table=True):
    stage_id: str = Field(nullable=False, primary_key=True, foreign_key="stage.id")
    user_id: str = Field(nullable=False, primary_key=True, foreign_key="user.id")


class StageQuery:

    @staticmethod
    def fetch(self, contest_id: str) -> list[dict]:
        return select(Stage).join(ContestStages).where(ContestStages.contest_id == contest_id)
