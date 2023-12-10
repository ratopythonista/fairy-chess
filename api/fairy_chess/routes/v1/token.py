from datetime import datetime

from fastapi import APIRouter, Body, HTTPException
from pydantic import BaseModel, Field, field_validator

from fairy_chess.database.user import UserModel
from fairy_chess.controllers.user import UserController

tornment_router = APIRouter(prefix="/tornment", tags=["admin"])


class TornmentRegisterRequest(BaseModel):
    name: str = Field(..., description="User email")
    starts_at: str = Field(..., description="Date for Tornment starts dd/mm/YYYY")

    @field_validator("starts_at")
    @classmethod
    def validate_starts_at(cls, starts_at) -> str:
        try:
            return datetime.strptime(starts_at, "%d/%m/%Y")
        except ValueError:
            raise HTTPException(403, "Invalid date format")   


@user_router.post('/register')
def register(user: UserModel = Body(..., description="User Registration Information")):
    return {"access_token": UserController(user).register()}


class UserRegisterRequest(BaseModel):
    email: str = Field(..., description="User email")
    password: str = Field(..., description="User password")


@user_router.post('/login')
def login(user: UserModel = Body(..., description="User Login Information")):
    return {"access_token": UserController(user).login()}
