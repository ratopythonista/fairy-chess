from uuid import uuid4
from loguru import logger
from peewee import IntegrityError
from bcrypt import hashpw, gensalt

from fairy_chess.models.user import UserModel
from fairy_chess.services.riot import RiotClient

class UserController:
    def register(username: str, email: str, password: str, summoner_name: str):
        try:
            salt = gensalt(rounds=12)
            hashed_password = hashpw(password.encode('utf8'), salt)
            summoner_puuid = RiotClient().get_puuid(summoner_name)
            UserModel.create(user_id=uuid4(), name=username, email=email, password=hashed_password, summoner_puuid=summoner_puuid)
        except IntegrityError:
            logger.error("USER ALREADY CREATED")