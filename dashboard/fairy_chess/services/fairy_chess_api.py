from enum import Enum
from pysondb import db
from requests import Session, Response

from fairy_chess.config import FAIRY_CHESS_API_PATH


class Endpoint(str, Enum):
    LOGIN       = "user/login"
    CONTESTS    = "contest"


class FairyChessAPI:
    def __init__(self) -> None:
        self.db = db.getDb("session.json")
        self.session = Session()
        self.session.headers = {"Content-Type": "application/json"}
        super().__init__()


class User(FairyChessAPI):
    def login(self, email: str, password: str, host: str) -> Response:
        host_session = self.db.getBy({"host": host})
        if not host_session:
            token = self.session.post(FAIRY_CHESS_API_PATH + Endpoint.LOGIN, json={"email": email, "password": password})
            access_token = token.json()["access_token"]
            self.db.add({"token": access_token, "host": host})


class Contest(FairyChessAPI):
    def fetch(self, host: str) -> Response:
        token_data = self.db.getBy({"host": host})
        if token_data:
            token_id = token_data[0].get("token")
            self.session.headers["X-Token"] = token_id
            response = self.session.get(FAIRY_CHESS_API_PATH + Endpoint.CONTESTS)
            if response.status_code == 403:
                self.db.deleteById(token_data[0].get("id"))
                return []
            return response.json()
        return []