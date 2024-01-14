from typing import Annotated

from fastapi import APIRouter, Body, Header

from fairy_chess.controllers.token import decode_token
from fairy_chess.controllers.user import UserController


user_router = APIRouter(prefix="/user", tags=["admin"])


@user_router.post('/register')
def register(email: Annotated[str, Body()], password: Annotated[str, Body()]):
    return {"access_token": UserController().register(email, password)}


@user_router.post('/login')
def login(email: Annotated[str, Body()], password: Annotated[str, Body()]):
    return {"access_token": UserController().login(email, password)}


@user_router.post('/link/riot')
def create(riot_id: str, x_token: Annotated[str, Header()] = None):
    user_id = decode_token(x_token)
    return UserController().link_riot(user_id, riot_id)