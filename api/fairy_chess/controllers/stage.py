from sqlmodel import Session

from fairy_chess.database import engine
# from fairy_chess.exceptions import ControllerException
from fairy_chess.database.models.stage import StageQuery


class StageController:
    def __init__(self) -> None:
        self.session = Session(engine)

    def fetch(self, contest_id: str) -> list[dict]:
        return [stage.model_dump() for stage in self.session.exec(StageQuery.fetch(contest_id)).all()]