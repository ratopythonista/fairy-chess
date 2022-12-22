from uuid import uuid4

from jose import jwe

from fairy_chess.config import API_KEY
from fairy_chess.services.riot import Riot
from fairy_chess.data import db_session, User, Summoner

@db_session
def put(name: str, email: str, password: str, summoner: str, user_id=str(uuid4())):
    summoner_info: dict = Riot().get_summoner(summoner)
    user = User(
        email=email, 
        name=name,
        password=jwe.encrypt(password, API_KEY, algorithm='dir', encryption='A128GCM').decode(),
    )
    Summoner(
        id=summoner_info.get("puuid"),
        summoner_id = summoner_info.get("id"),
        account_id = summoner_info.get("accountId"),
        user = user,
        name = summoner,
        profile_icon = summoner_info.get("profileIconId"),
        revision_date = summoner_info.get("revisionDate")
    )
    return True


@db_session
def get(user_id: str):
    return User[user_id]

@db_session
def authenticate(email: str, password: str):
    user: User = User.get(email=email)
    if user:
        password_stored = jwe.decrypt(user.password, API_KEY).decode()
        if password == password_stored:
            return user.id