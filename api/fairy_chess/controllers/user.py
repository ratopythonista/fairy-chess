from fastapi import HTTPException

from fairy_chess.controllers.token import Token
from fairy_chess.database.user import user_repository, UserModel


class UserController:
    def __init__(self, user: UserModel) -> None:
        self.user: UserModel = UserModel(**user.model_dump())

    def register(self):
        base_user = user_repository.find_by_riot_id(self.user.riot_id)
        if not base_user and user_repository.save(self.user):
            return Token.new(self.user)
        raise HTTPException(status_code=403, detail="User alredy exists")

    def login(self):
        base_user = user_repository.find_by_email(self.user.email)
        if base_user == self.user:
            return Token.new(base_user)
        raise HTTPException(status_code=403, detail="User/Password invalid")
