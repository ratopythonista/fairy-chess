import re
import hmac

from sqlmodel import Session

from fairy_chess.config import HASH_KEY
from fairy_chess.database import engine
from fairy_chess.controllers.token import encode_token
from fairy_chess.database.models.user import User, UserQuery

from fairy_chess.exceptions import ControllerException

EMAIL_RE = r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'
PWD_RE = r'[\d|\w|]{8,}'

class UserController:
    def __init__(self) -> None:
        self.session = Session(engine)

    def link_riot(self, user_id: str, riot_id: str) -> dict:
        user = self.session.exec(UserQuery.find_by_id(user_id)).first()
        if user:
            user.riot_id = riot_id
            self.session.add(user)
            self.session.commit()
            self.session.refresh(user)
            return user.model_dump(exclude={'password', 'id'})
        raise ControllerException(status_code=404, detail="User not found")
        
    def register(self, email: str, password: str) -> str:
        try:
            if re.fullmatch(EMAIL_RE, email) and re.fullmatch(PWD_RE, password):
                hash_password = hmac.new(HASH_KEY.encode(), password.encode(), 'sha256').digest()
                user = User(email=email, password=hash_password)
                self.session.add(user)
                self.session.commit()
                self.session.refresh(user)
                return encode_token(user.id)
            raise ControllerException(status_code=403, detail="Invalid Email/Password")
        except:
            raise ControllerException(status_code=403, detail="User alredy exists")

    def login(self, email: str, password: str) -> str:
        user = self.session.exec(UserQuery.find_by_email(email)).first()
        hash_password = hmac.new(HASH_KEY.encode(), password.encode(), 'sha256').digest()
        if user and hmac.compare_digest(user.password, hash_password):
            return encode_token(user.id)
        raise ControllerException(status_code=403, detail="User/Password invalid")

