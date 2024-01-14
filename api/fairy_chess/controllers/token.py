from uuid import UUID

import jwt
from datetime import datetime, timedelta

from fairy_chess.config import JWT_KEY
from fairy_chess.exceptions import TokenException

def encode_token(user_id: UUID) -> str:
    expires_at = datetime.now() + timedelta(hours=12)
    payload = dict(user_id=user_id, expires_at=expires_at.timestamp())
    return jwt.encode(payload, JWT_KEY, algorithm="HS256")

def decode_token(token: str) -> UUID:
    payload: dict = jwt.decode(token, JWT_KEY, algorithms=["HS256"])
    if payload.get("expires_at") < datetime.now().timestamp():
        raise TokenException(403, "Token expired")
    return payload.get("user_id")