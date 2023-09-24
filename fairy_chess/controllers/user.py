from uuid import uuid4
from loguru import logger
from peewee import IntegrityError
from cryptography.fernet import Fernet

from fairy_chess.models.user import UserModel
from fairy_chess.services.riot import RiotClient
from fairy_chess.config import HASH_KEY

class UserController:
    fernet = Fernet(HASH_KEY)

    def register(username: str, email: str, password: str, summoner_name: str):
        try:
            hashed_password = UserController.fernet.encrypt(password.encode('utf8'))
            summoner_puuid = RiotClient().get_puuid(summoner_name)
            UserModel.create(user_id=uuid4(), name=username, email=email, password=hashed_password, summoner_puuid=summoner_puuid)
        except IntegrityError:
            logger.error("USER ALREADY CREATED")

    def login(username: str, password: str):
        try:
            user: UserModel = UserModel.get(UserModel.name == username)
            decoded_password = UserController.fernet.decrypt(user.password)
            if decoded_password.decode() == password:
                return user
            logger.error("PASSWORD IS INVALID")
        except:
            logger.error("USER DOES NOT EXIST")

