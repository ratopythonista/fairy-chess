from sqlmodel import Session

from fairy_chess.database import engine
from fairy_chess.exceptions import ControllerException
from fairy_chess.database.models.stage import StageQuery, Stage, Contest


class StageController:
    def __init__(self) -> None:
        self.session = Session(engine)

    def fetch(self, contest_id: str) -> list[dict]:
        return [stage.model_dump() for stage in self.session.exec(StageQuery.fetch(contest_id)).all()]
    
    def update(self, user_id: str, stage_id: str, start_players: int = None, qtd_rounds: int = None, shuffle_rate: int = None):
        try:
            stage: Stage = self.session.exec(StageQuery.find_by_id(stage_id=stage_id)).first()
            contest: Contest = self.session.exec(StageQuery.get_contest(stage_id=stage_id)).first()
            if contest.creator == user_id:
                if start_players is not None:
                    stage.start_players = start_players
                if qtd_rounds is not None:
                    stage.qtd_rounds = qtd_rounds
                if shuffle_rate is not None:
                    stage.shuffle_rate = shuffle_rate
                self.session.add(stage)
                self.session.commit()
                self.session.refresh(stage)
                return stage
        except Exception as e:
            raise ControllerException(404, f"Couldnt update stage: {e}")
