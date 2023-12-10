import re
import hmac

from fastapi import HTTPException
from pydantic import BaseModel, Field, field_validator
from pydantic_mongo import ObjectIdField, AbstractRepository

from fairy_chess.config import HASH_KEY
from fairy_chess.database import database


class UserModel(BaseModel):
    id: ObjectIdField = None
    email: str = Field(..., description="User email")
    password: str | bytes = Field(..., description="User password")
    riot_id: str = Field('', description="User riot id (name#id)")
    
    @field_validator("email")
    @classmethod
    def validate_email(cls, email) -> str:
        regex = r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'
        if re.fullmatch(regex, email):
            return email
        raise HTTPException(403, "Invalid email")    
    
    @field_validator("password")
    @classmethod
    def validate_password(cls, password: str | bytes) -> str:
        regex = r'[\d|\w|]{8,}'
        if isinstance(password, bytes):
            return password        
        elif re.fullmatch(regex, password):
            return hmac.new(HASH_KEY.encode(), password.encode(), 'sha256').digest()        
        raise HTTPException(403, "Invalid password")
    
    def __eq__(self, other: 'UserModel') -> bool:
        return self.email == other.email and hmac.compare_digest(self.password, other.password) 


class UserRepository(AbstractRepository[UserModel]):
   
    def find_by_riot_id(self, riot_id: str):
        return self.find_one_by({"riot_id": riot_id})

    def find_by_email(self, email: str):
        return self.find_one_by({"email": email})

    class Meta:
        collection_name = 'user'

user_repository = UserRepository(database=database)