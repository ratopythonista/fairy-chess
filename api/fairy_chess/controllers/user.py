import hmac

from fastapi import HTTPException

from fairy_chess.config import HASH_KEY
from fairy_chess.controllers.token import Token, JWT
from fairy_chess.services.riot import RiotService, Summoner, RiotId
from fairy_chess.database.user import user_repository, UserModel



class UserController:
    def __init__(self, user: UserModel) -> None:
        self.user: UserModel = UserModel(**user.model_dump())

    def register(email: str, password: str, riot_id: str) -> JWT:
        name, tag = riot_id.split("#")
        summoner: Summoner = RiotService().get_summoner(RiotId(name=name, tag=tag))
        base_user = user_repository.find_by_riot_id(summoner.puuid)
        if not base_user:
            user_repository.save(UserModel(email=email, password=password, summoner=summoner))
            return Token.encode(summoner)
        raise HTTPException(status_code=403, detail="User alredy exists")

    def login(email: str, password: str) -> JWT:
        base_user = user_repository.find_by_email(email)
        hash_password = hmac.new(HASH_KEY.encode(), password.encode(), 'sha256').digest()
        if base_user and hmac.compare_digest(base_user.password, hash_password):
            return Token.encode(base_user.summoner)
        raise HTTPException(status_code=403, detail="User/Password invalid")
