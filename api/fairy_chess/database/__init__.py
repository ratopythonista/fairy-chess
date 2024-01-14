from sqlmodel import SQLModel, create_engine

from fairy_chess.database.models.user import User # noqa
from fairy_chess.config import PGSQL_URI

engine = create_engine(PGSQL_URI)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def session_factory():
    return 