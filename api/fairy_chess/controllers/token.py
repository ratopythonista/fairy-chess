import jwt
from pydantic import BaseModel
from fastapi import HTTPException
from datetime import datetime, timedelta

from fairy_chess.config import JWT_KEY
from fairy_chess.services.riot import Riot
from fairy_chess.database.user import UserModel

class Token(BaseModel):
    riot_id: str
    icon_id: str
    current_rank: str

    def new(user: UserModel):
        riot = Riot(user.riot_id)
        
        icon_id: str = riot.icon
        current_rank: str = riot.rank
        expires_at = datetime.now() + timedelta(minutes=5)
        payload = {"riot_id": user.riot_id, "icon_id": icon_id, "current_rank": current_rank, "expires_at": expires_at}
        return jwt.encode(payload, JWT_KEY, algorithm="HS256")
    
    def decode(token: str):
        payload: dict = jwt.decode(token)
        if payload.get("exires_at") > datetime.now():
            raise HTTPException(403, "Token expired")
        return Token(payload)