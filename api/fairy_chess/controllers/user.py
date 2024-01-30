import re
import hmac
from uuid import uuid4

from sqlmodel import Session

from fairy_chess.config import HASH_KEY
from fairy_chess.controllers import BaseController
from fairy_chess.controllers.token import encode_token
from fairy_chess.database.models.user import User, UserRepository

from fairy_chess.exceptions import ControllerException

EMAIL_RE = r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'
PWD_RE = r'[\d|\w|]{8,}'

class UserController(BaseController):
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

