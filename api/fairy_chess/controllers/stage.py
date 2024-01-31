from fairy_chess.controllers import BaseController
from fairy_chess.exceptions import ControllerException
from fairy_chess.database.models.contest import ContestQuery
from fairy_chess.database.models.stage import StageRepository, Stage, Contest, StageUser


class StageController(BaseController):
    def __insert_stage_user(self, stage_id: str, user_id: str) -> StageUser:
        stage_user = StageUser(stage_id=stage_id, user_id=user_id)
        self.session.add(stage_user)
        self.session.commit()
        self.session.refresh(stage_user)
        return stage_user
    
    def __check_ownership(self, contest_id: str, user_id: str):
        contest: Contest = self.session.exec(ContestQuery.find_by_id(contest_id=contest_id)).first()
        if contest.creator != user_id:
            raise ControllerException(403, f"Only the creator can start the stage")


    def fetch(self, contest_id: str) -> list[dict]:
        return [stage.model_dump() for stage in self.session.exec(StageRepository.fetch(contest_id)).all()]
    


