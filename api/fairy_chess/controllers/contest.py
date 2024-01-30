from uuid import uuid4
from datetime import datetime, timedelta

from fairy_chess.exceptions import ControllerException
from fairy_chess.database.models.contest import Contest, ContestUser, ContestRepository


class ContestController:
    def create(self, title: str, timestamp: float, start_players: int, user_id: str):
        try:
            return ContestRepository().new_contest(title, timestamp, start_players, user_id)
        except:
            raise ControllerException(status_code=403, detail="Contest alredy exists")

    def fetch(self, user_id: str = None) -> list[dict]:
        return ContestRepository().find_all(user_id)

    def competitors(self, contest_id: str, check_in: bool | None = None):
        return ContestRepository().competitors(contest_id, check_in)

    def register(self, contest_id: str, user_id: str) -> dict:
        try:
            return ContestRepository().register(contest_id, user_id)
        except:
            raise ControllerException(status_code=403, detail="User alredy register in this tournment")

    def check_in(self, contest_id: str, user_id: str):
        contest_repository = ContestRepository()
        contest: Contest = contest_repository.find_by_id(contest_id)
        if (
            contest_repository.is_registred(contest_id=contest_id, user_id=user_id) 
            and not datetime.now().timestamp() < contest.timestamp - timedelta(minutes=30)
        ):
            return contest_repository.check_in(contest_id, user_id)
        raise ControllerException(status_code=403, detail="Check In Error")
    
    def start(self, contest_id: str, user_id: str):
        contest_repository = ContestRepository()
        contest: Contest = contest_repository.find_by_id(contest_id)
        if contest.creator == user_id:
            pass
        raise ControllerException(status_code=403, detail="Start Error")
