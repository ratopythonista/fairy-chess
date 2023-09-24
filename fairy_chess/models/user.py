from peewee import CharField, UUIDField, TextField, BooleanField

from fairy_chess.models import BaseModel

class UserModel(BaseModel):
    user_id = UUIDField(unique=True)
    name = TextField()
    email = TextField()
    password = TextField()
    is_verified = BooleanField(default=False)
    summoner_puuid = CharField(78)