from peewee import CharField, UUIDField, TextField, BooleanField

from fairy_chess.models import BaseModel

class UserModel(BaseModel):
    user_id = UUIDField(primary_key=True)
    name = TextField(unique=True)
    email = TextField(unique=True)
    password = TextField()
    is_verified = BooleanField(default=False)
    summoner_puuid = CharField(78, unique=True)