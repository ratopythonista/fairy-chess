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
    contest_id: str = Field(nullable=False, foreign_key="contest.id")


class StageUser(SQLModel, table=True):
    stage_id: str = Field(nullable=False, primary_key=True, foreign_key="stage.id")
    user_id: str = Field(nullable=False, primary_key=True, foreign_key="user.id")
    check_in: Optional[bool] = Field(default=False, primary_key=True)


class StageRepository(BaseRepository):
    def new_stage(self, title: str, start_players: int, contest_id: str) -> Stage:
        stage = Stage(id=str(uuid4()), title=title, start_players=start_players, contest_id=contest_id)
        self.session.add(stage)
        self.session.commit()
        self.session.refresh(stage)
        return stage
    
    def new_stage_user(self, stage_id: str, user_id: str) -> StageUser:
        stage_user = StageUser(stage_id=stage_id, user_id=user_id)
        self.session.add(stage_user)
        self.session.commit()
        self.session.refresh(stage_user)
        return stage_user
    
    def init_stage(self, contest_id: str, competitors: list[dict]) -> list[StageUser]:
        stage: Stage = self.new_stage(f'TOP{len(competitors)}', len(competitors), contest_id)
        return [self.new_stage_user(stage_id=stage.id, user_id=competitor['user_id']) for competitor in competitors]
            