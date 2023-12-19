import jwt
from fastapi import HTTPException
from pydantic import BaseModel, Field
from datetime import datetime, timedelta

from fairy_chess.config import JWT_KEY
from fairy_chess.services.riot import Summoner

class JWT(BaseModel):
    puuid: str = Field(..., description="Public User Uniq ID")
    expires_at: float = Field(..., description="Token Expire Data")

class Token:
    def encode(summoner: Summoner) -> str:
        expires_at = datetime.now() + timedelta(hours=12)
        payload = JWT(puuid=summoner.puuid, expires_at=expires_at.timestamp())
        return jwt.encode(payload.model_dump(), JWT_KEY, algorithm="HS256")
    
    def decode(token: str) -> JWT:
        payload: dict = jwt.decode(token, JWT_KEY, algorithms=["HS256"])
        if payload.get("expires_at") < datetime.now().timestamp():
            raise HTTPException(403, "Token expired")
        return JWT(**payload)