from fastapi import APIRouter, Body
from loguru import logger
from fairy_chess.database.user import User, RiotUser
from fairy_chess.controllers.user import UserController

user_router = APIRouter(prefix="/user", tags=["admin"])


@user_router.post('/register')
def register(user_data: User = Body(..., description="User Registration Information")):
    logger.debug(user_data)
    return {"access_token": UserController().register(user_data)}


@user_router.post('/login')
def login(user_data: User = Body(..., description="User Login Information")):
    return {"access_token": UserController().login(user_data)}

@user_router.get('/')
def get_summoner_data():
    return UserController().get_summoner_data()