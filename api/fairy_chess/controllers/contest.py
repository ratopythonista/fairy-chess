from uuid import uuid4

from sqlmodel import Session

from fairy_chess.database import engine
from fairy_chess.exceptions import ControllerException
from fairy_chess.database.models.stage import Stage, ContestStages
from fairy_chess.database.models.contest import Contest, ContestUser, ContestQuery


class ContestController:
    def __init__(self) -> None:
        self.session = Session(engine)

    def __del__(self) -> None:
        self.session.close()

    def create(self, title: str, timestamp: float, size: int, qtd_rounds: int, shuffle_rate: int, user_id: str):
        try:
            contest = Contest(id=str(uuid4()), title=title, timestamp=timestamp, size=size, creator=user_id)
            self.session.add(contest)
            self.session.commit()
            self.session.refresh(contest)

            stage_list: list[Stage] = list()
            while size >= 8:
                stage = Stage(id=str(uuid4()), title=f"TOP{size}", start_players=size, qtd_rounds=qtd_rounds, shuffle_rate=shuffle_rate)
                stage_list.append(stage)
                size = size // 2
            
            for stage in stage_list:
                contest_stage = ContestStages(contest_id=contest.id, stage_id=stage.id)
                self.session.add(stage)
                self.session.commit()
                self.session.add(contest_stage)
                self.session.commit()

            self.session.refresh(contest)
            
            return contest.model_dump()
        except:
            raise ControllerException(status_code=403, detail="Contest alredy exists")

    def fetch(self, user_id: str = None) -> list[dict]:
        return self.session.exec(
            ContestQuery.find_all(user_id)
        ).first().model_dump(
            exclude={"creator"} if user_id else {}
        )

    def competitors(self, contest_id: str, check_in: bool | None = None):
        return [
            user.model_dump(exclude={'password', 'id'}) 
            for user in self.session.exec(ContestQuery.competitors(contest_id, check_in)).all()
        ]

    def register(self, contest_id: str, user_id: str):
        try:
            contest_user = ContestUser(contest_id=contest_id, user_id=user_id)
            self.session.add(contest_user)
            self.session.commit()
            self.session.refresh(contest_user)
            return contest_user.model_dump()
        except:
            raise ControllerException(status_code=403, detail="User alredy register in this tournment")


    def check_in(self, contest_id: str, user_id: str):
        contest_user = self.session.exec(ContestQuery.find_registred(contest_id, user_id)).first()
        if contest_user and not contest_user.check_in:
            contest_user.check_in = True
            self.session.commit()
            self.session.refresh(contest_user)
            return contest_user.model_dump()
        raise ControllerException(status_code=403, detail="Check In Error")