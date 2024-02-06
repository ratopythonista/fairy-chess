from uuid import uuid4

from typing import Optional
from sqlmodel import Field, SQLModel, select

from fairy_chess.database import BaseRepository
from fairy_chess.database.models.lobby import LobbyUser, Lobby


class Match(SQLModel, table=True):
    id: Optional[str] = Field(default=str(uuid4()), primary_key=True)
    title: str = Field(index=True, nullable=False, unique=False)
    is_sync: bool = Field(default=False, nullable=False)
    riot_id: str = Field(nullable=True)

    lobby_id: str = Field(nullable=False, foreign_key="lobby.id")


class MatchUser(SQLModel, table=True):
    match_id: str = Field(nullable=False, primary_key=True, foreign_key="match.id")
    user_id: str = Field(nullable=False, primary_key=True, foreign_key="user.id")
    placement: int = Field(nullable=False)


class MatchRepository(BaseRepository):
    def get_match_user(self, match_id: str):
        return self.session.exec(select(MatchUser).where(MatchUser.match_id == match_id)).all()

    def fetch_by_stage(self, stage_id: str) -> list[Match]:
        return self.session.exec(select(Match).join(Lobby).where(Lobby.stage_id == stage_id)).all()

    def new_match(self, title: str, lobby_id: str, match_riot_id: str) -> Match:
        match = Match(id=str(uuid4()), title=title, lobby_id=lobby_id, riot_id=match_riot_id)
        self.session.add(match)
        self.session.commit()
        self.session.refresh(match)
        return match

    def new_match_user(self, match_id: str, user_id: str, placement: int) -> MatchUser:
        match_user = MatchUser(match_id=match_id, user_id=user_id, placement=placement)
        self.session.add(match_user)
        self.session.commit()
        self.session.refresh(match_user)
        return match_user
    
    def init_match(self, title: str, match_riot_id: str, lobby_id: str, competitors: list[str], placements: list[str]) -> list[MatchUser]:
        match: Match = self.new_match(title, lobby_id, match_riot_id)
        return [
            self.new_match_user(match_id=match.id, user_id=competitor, placement=placement)
            for competitor, placement in zip(competitors, placements)
        ]