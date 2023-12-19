from typing import Annotated
from datetime import datetime

from pydantic import BaseModel, Field, field_validator
from fastapi import APIRouter, Body, HTTPException, Header

from fairy_chess.controllers.token import Token, JWT
from fairy_chess.controllers.tournment import TournmentController   

tournment_router = APIRouter(prefix="/tournemt", tags=["admin"])


class RegisterRequest(BaseModel):
    name: str = Field(..., description="User email")
    starts_at: float | str = Field(..., description="Date for Tournemt starts dd/mm/YYYY")

    @field_validator("starts_at")
    @classmethod
    def validate_starts_at(cls, starts_at) -> str:
        try:
            return datetime.strptime(starts_at, "%d/%m/%Y").timestamp()
        except ValueError:
            raise HTTPException(403, "Invalid date format")   


@tournment_router.post('/create')
def create(tournment: RegisterRequest = Body(), x_token: Annotated[str, Header()] = None):
    jwt: JWT = Token.decode(x_token)
    return TournmentController.create(**tournment.model_dump(), puuid=jwt.puuid)


@tournment_router.get('/')
def fetch(x_token: Annotated[str, Header()] = None,):
    jwt: JWT = Token.decode(x_token)
    return TournmentController.fetch()


@tournment_router.post('/register/{tournment_id}')
def register(tournment_id: str, x_token: Annotated[str, Header()] = None,):
    jwt: JWT = Token.decode(x_token)
    return TournmentController.register(tournment_id, jwt.puuid)