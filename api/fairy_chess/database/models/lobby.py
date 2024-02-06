from uuid import uuid4

from typing import Optional
from sqlmodel import Field, SQLModel, select

from fairy_chess.database import BaseRepository
from fairy_chess.database.models.stage import StageUser


class Lobby(SQLModel, table=True):
    id: Optional[str] = Field(default=str(uuid4()), primary_key=True)
    title: str = Field(index=True, nullable=False, unique=False)
    stage_id: str = Field(nullable=False, foreign_key="stage.id")


class LobbyUser(SQLModel, table=True):
    lobby_id: str = Field(nullable=False, primary_key=True, foreign_key="lobby.id")
    user_id: str = Field(nullable=False, primary_key=True, foreign_key="user.id")
    check_in: Optional[bool] = Field(default=False, primary_key=True)


class LobbyRepository(BaseRepository):
    def fetch_by_stage_id(self, stage_id: str) -> list[Lobby]:
        return self.session.exec(select(Lobby).where(Lobby.stage_id == stage_id)).all()

    def competitors(self, lobby_id: str) -> list[StageUser]:
        return self.session.exec(select(LobbyUser).where(LobbyUser.lobby_id == lobby_id)).all()

    def new_lobby(self, title: str, stage_id: str) -> Lobby:
        lobby = Lobby(id=str(uuid4()), title=title, stage_id=stage_id)
        self.session.add(lobby)
        self.session.commit()
        self.session.refresh(lobby)
        return lobby
    
    def new_lobby_user(self, lobby_id: str, user_id: str) -> LobbyUser:
        lobby_user = LobbyUser(lobby_id=lobby_id, user_id=user_id)
        self.session.add(lobby_user)
        self.session.commit()
        self.session.refresh(lobby_user)
        return lobby_user
    
    def init_lobby(self, title: str, stage_id: str, competitors: list[StageUser]) -> list[LobbyUser]:
        lobby: Lobby = self.new_lobby(title, stage_id)
        return [self.new_lobby_user(lobby_id=lobby.id, user_id=competitor.user_id) for competitor in competitors]