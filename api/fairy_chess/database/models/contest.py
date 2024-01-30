from uuid import uuid4

from typing import Optional
from sqlmodel import Field, SQLModel, select

from fairy_chess.database import BaseRepository
from fairy_chess.database.models.user import User


class Contest(SQLModel, table=True):
    id: Optional[str] = Field(default=str(uuid4()), primary_key=True)
    title: str = Field(index=True, nullable=False, unique=True)
    timestamp: float = Field(nullable=False)
    start_players: int = Field(nullable=False)
    qtd_matches: int = Field(nullable=False)
    shuffle_rate: int = Field(nullable=False)

    creator: Optional[str] = Field(nullable=False, foreign_key="user.id")


class ContestUser(SQLModel, table=True):
    contest_id: str = Field(nullable=False, primary_key=True, foreign_key="contest.id")
    user_id: str = Field(nullable=False, primary_key=True, foreign_key="user.id")
    check_in: Optional[bool] = Field(default=False, primary_key=True)


class ContestRepository(BaseRepository):
    def find_all(self, user_id: str = None) -> list[dict]:
        query = select(Contest)
        if user_id:
            query.where(Contest.creator == user_id)
        return [contest.model_dump() for contest in self.session.exec(query).all()]

    def find_by_id(self, contest_id: str) -> dict:
        return self.session.exec(select(Contest).where(Contest.id == contest_id)).first().model_dump()

    def competitors(self, contest_id: str, check_in: bool | None = None) -> list[dict]:
        query = select(User).join(ContestUser).where(ContestUser.contest_id == contest_id)
        if check_in == True:
            return query.where(ContestUser.check_in == True)
        return [
            user.model_dump(exclude={'password', 'id'}) 
            for user in self.session.exec(query).all()
        ]

    def is_registred(self, contest_id: str, user_id: str) -> str:
        return self.session.exec(select(ContestUser).where(
            ContestUser.contest_id == contest_id, ContestUser.user_id == user_id
        )).first() is not None

    def new_contest(self, title: str, timestamp: float, start_players: int, creator: str) -> dict:
        contest =  Contest(
            id=str(uuid4()), 
            title=title, 
            timestamp=timestamp, 
            start_players=start_players, 
            creator=creator, 
            qtd_matches=6, 
            shuffle_rate=2
        )
        self.session.add(contest)
        self.session.commit()
        self.session.refresh(contest)
        return contest.model_dump()

    def register(self, contest_id: str, user_id: str) -> dict:
        contest_user = ContestUser(contest_id=contest_id, user_id=user_id)
        self.session.add(contest_user)
        self.session.commit()
        self.session.refresh(contest_user)
        return contest_user.model_dump()

    def check_in(self, contest_id: str, user_id: str):
        contest_user: ContestUser = self.session.exec(select(ContestUser).where(
            ContestUser.contest_id == contest_id, ContestUser.user_id == user_id
        )).first()
        contest_user.check_in = True
        self.session.commit()
        self.session.refresh(contest_user)
        return contest_user.model_dump()