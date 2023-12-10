from typing import Annotated
from datetime import datetime

from pydantic import BaseModel, Field, field_validator
from fastapi import APIRouter, Body, HTTPException, Header

from fairy_chess.controllers.token import Token
from fairy_chess.controllers.tournment import TournmentController   

tournment_router = APIRouter(prefix="/tournemt", tags=["admin"])


class tournmentRegisterRequest(BaseModel):
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
def create(
    x_token: Annotated[str, Header()] = None,
    tournment: Annotated[tournmentRegisterRequest, Body(..., description="Tournemt Register Request")] = None 
):
    return TournmentController(Token.decode(x_token), tournment).create()


@tournment_router.get('/')
def fetch(x_token: Annotated[str, Header()] = None,):
    return TournmentController(Token.decode(x_token)).fetch()


@tournment_router.post('/register')
def register(x_token: Annotated[str, Header()] = None,):
    return TournmentController(Token.decode(x_token)).register()