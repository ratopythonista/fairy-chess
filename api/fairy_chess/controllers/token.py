import jwt
from pydantic import BaseModel
from fastapi import HTTPException
from datetime import datetime, timedelta

from fairy_chess.config import JWT_KEY
from fairy_chess.services.riot import Riot
from fairy_chess.database.user import UserModel

class Token(BaseModel):
    riot_id: str
    icon_id: str | int
    current_rank: str

    def new(user: UserModel):
        riot = Riot(user.riot_id)
        
        icon_id: str = riot.icon
        current_rank: str = riot.rank
        expires_at = datetime.now() + timedelta(hours=12)
        payload = {
            "icon_id": icon_id,
            "riot_id": user.riot_id,
            "current_rank": current_rank,
            "expires_at": expires_at.timestamp()
        }
        return jwt.encode(payload, JWT_KEY, algorithm="HS256")
    
    def decode(token: str):
        payload: dict = jwt.decode(token, JWT_KEY, algorithms=["HS256"])
        if payload.get("expires_at") < datetime.now().timestamp():
            raise HTTPException(403, "Token expired")
        return Token(**payload)