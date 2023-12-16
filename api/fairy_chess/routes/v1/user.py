from pydantic import BaseModel, Field

from fastapi import APIRouter, Body
from fairy_chess.database.user import UserModel
from fairy_chess.controllers.user import UserController

user_router = APIRouter(prefix="/user", tags=["admin"])


class UserRegisterRequest(BaseModel):
    email: str = Field(..., description="User email")
    password: str = Field(..., description="User password")
    riot_id: str = Field('', description="User riot id (name#id)")


@user_router.post('/register')
def register(user: UserRegisterRequest = Body(..., description="User Registration Information")):
    return {"access_token": UserController(user).register()}


class UserLoginRequest(BaseModel):
    email: str = Field(..., description="User email")
    password: str = Field(..., description="User password")


@user_router.post('/login')
def login(user: UserLoginRequest = Body(..., description="User Login Information")):
    return {"access_token": UserController(user).login()}
