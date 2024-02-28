import re
import hmac

from fastapi import Header
from typing import Annotated

from fairy_chess.config import HASH_KEY
from fairy_chess.database.models.user import UserRepository, User
from fairy_chess.controllers.token import encode_token, decode_token

from fairy_chess.exceptions import ControllerException

EMAIL_RE = r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'
PWD_RE = r'[\d|\w|]{8,}'

class UserController:
    def link_riot(self, user_id: str, riot_id: str) -> dict:
        return UserRepository().update_riot_id(user_id, riot_id)

    def register(self, email: str, password: str) -> str:
        if re.fullmatch(EMAIL_RE, email) and re.fullmatch(PWD_RE, password):
            hash_password: bytes = hmac.new(HASH_KEY.encode(), password.encode(), 'sha256').digest()
            user = UserRepository().new_user(email, hash_password)
            return encode_token(user.id)
        raise ControllerException(status_code=403, detail="Invalid Email/Password")

    def login(self, email: str, password: str) -> str:
        user = UserRepository().find_by_email(email)
        hash_password = hmac.new(HASH_KEY.encode(), password.encode(), 'sha256').digest()
        if user and hmac.compare_digest(user.password, hash_password):
            return encode_token(user.id)
        raise ControllerException(status_code=403, detail="User/Password invalid")

    @classmethod
    def get_from_token(cls, authorization: Annotated[str, Header()] = '') -> User:
        user_id = decode_token(authorization.split()[1])
        return UserRepository().find_by_id(user_id)
