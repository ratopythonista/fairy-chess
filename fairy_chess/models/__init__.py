from peewee import PostgresqlDatabase, Model

from fairy_chess.config import DATABSE_URI

psql_db = PostgresqlDatabase(DATABSE_URI)

class BaseModel(Model):
    """A base model that will use our Postgresql database"""
    class Meta:
        database = psql_db