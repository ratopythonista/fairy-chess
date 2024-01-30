from sqlmodel import SQLModel, create_engine, Session

from fairy_chess.config import PGSQL_URI

engine = create_engine(PGSQL_URI)

class BaseRepository:
    def __init__(self) -> None:
        self.session = Session(engine)

    def __del__(self) -> None:
        self.session.close()

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)