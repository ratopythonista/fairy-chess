from pydantic import BaseModel

from fastapi import APIRouter

from fairy_chess.controllers.token import JWT
from fairy_chess.controllers.user import UserController

user_router = APIRouter(prefix="/user", tags=["admin"])


class RegisterModel(BaseModel):
    email: str
    password: str
    riot_id: str


@user_router.post('/register')
def register(body: RegisterModel):
    return {"access_token": UserController.register(**body.model_dump())}


class RegisterModel(BaseModel):
    email: str
    password: str

@user_router.post('/login')
def login(body: RegisterModel):
    return {"access_token": UserController.login(**body.model_dump())}
