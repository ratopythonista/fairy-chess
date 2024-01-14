from uuid import uuid4

from typing import Optional
from sqlmodel import Field, SQLModel, select


# TODO change username for email in ERD
class User(SQLModel, table=True):
    id: Optional[str] = Field(default=str(uuid4()), primary_key=True)
    email: str = Field(index=True, nullable=False, unique=True)
    password: Optional[bytes] = Field(nullable=False)
    riot_id: Optional[str] = Field(nullable=True, unique=True)
    
class UserQuery:
    @staticmethod
    def find_by_email(email: str):
        return select(User).where(User.email == email)
    
    @staticmethod
    def find_by_id(user_id: str):
        return select(User).where(User.id == user_id)