from sqlmodel import Session

from fairy_chess.database import engine

class BaseController:
    def __init__(self) -> None:
        self.session = Session(engine)

    def __del__(self) -> None:
        self.session.close() 