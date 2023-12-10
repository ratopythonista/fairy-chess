import jwt
from fastapi import HTTPException

from fairy_chess.config import JWT_KEY
from fairy_chess.services.riot import Riot
from fairy_chess.database.user import user_repository, UserModel


class UserController:
    def __init__(self, user: UserModel) -> None:
        self.user: UserModel = user

    def register(self):
        base_user = user_repository.find_by_riot_id(self.user.riot_id)
        if not base_user and user_repository.save(self.user):
            return self.get_token()
        raise HTTPException(status_code=403, detail="User alredy exists", headers={"user": self.user.riot_id})

    def login(self):
        base_user = user_repository.find_by_email(self.user.email)
        if base_user == self.user:
            self.user = base_user
            return self.get_token()
        raise HTTPException(status_code=403, detail="User/Password invalid", headers={"user": self.user.riot_id})
        
    def get_token(self):
        riot = Riot(self.user.riot_id)
        icon_id: str = riot.icon
        current_rank: str = riot.rank
        payload = {"riot_id": self.user.riot_id, "icon_id": icon_id, "current_rank": current_rank}
        return jwt.encode(payload, JWT_KEY, algorithm="HS256")
