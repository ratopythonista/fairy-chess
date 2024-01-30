from uuid import uuid4

from typing import Optional
from sqlmodel import Field, SQLModel, select

from fairy_chess.database import BaseRepository


class User(SQLModel, table=True):
    id: Optional[str] = Field(default=str(uuid4()), primary_key=True)
    email: str = Field(index=True, nullable=False, unique=True)
    password: Optional[bytes] = Field(nullable=False)
    riot_id: Optional[str] = Field(nullable=True, unique=True)


class UserRepository(BaseRepository):
    def new_user(self, email: str, password: bytes) -> User:
        user = User(id=str(uuid4()), email=email, password=password)
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def find_by_email(self, email: str) -> User:
        return self.session.exec(select(User).where(User.email == email)).first()

    def update_riot_id(self, user_id: str, riot_id: str) -> dict:
        user = self.session.exec(UserRepository.find_by_id(select(User).where(User.id == user_id))).first()
        user.riot_id = riot_id
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user.model_dump(exclude={'password', 'id'})