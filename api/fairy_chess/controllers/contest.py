from datetime import datetime

from sqlmodel import Session

from fairy_chess.database import engine
from fairy_chess.exceptions import ControllerException
from fairy_chess.database.models.contest import Contest, ContestQuery





class ContestController:
    def __init__(self) -> None:
        self.session = Session(engine)

    def create(self, title: str, timestamp: float, size: int, user_id: str):
        try:
            contest = Contest(title=title, timestamp=timestamp, size=size, creator=user_id)
            self.session.add(contest)
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

    # def register(tournment_id: str, puuid: str):
    #     tournment_base = tournment_repository.find_one_by_id(tournment_id)
    #     if tournment_base and puuid not in tournment_base.competitors:
    #         tournment_base.competitors.append(puuid)
    #         tournment_repository.save(tournment_base)
    #         return tournment_base
    #     raise HTTPException(status_code=403, detail="User alredy register in this tournment")