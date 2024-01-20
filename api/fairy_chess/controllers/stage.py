from uuid import uuid4
from random import shuffle

from sqlmodel import Session
from pydantic import BaseModel

from fairy_chess.database import engine
from fairy_chess.exceptions import ControllerException
from fairy_chess.database.models.stage import StageQuery, Stage, Contest, User
from fairy_chess.database.models.match import Match, MatchQuery, MatchUser


class MatchDetail(BaseModel):
    match_id: str
    title: str
    participants: list[str]


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

    def matches(self, stage_id: str):
        try:
            stage: Stage = self.session.exec(StageQuery.find_by_id(stage_id=stage_id)).first()
            user_list: list[User] = self.session.exec(StageQuery.get_users(stage_id=stage_id)).all()
            match_list: list[dict] = []
            while user_list:
                qtd_matches: int = self.session.exec(MatchQuery.find_stage_matches(stage_id=stage_id)).all().count()
                match = Match(id=str(uuid4()), title=f'Match {stage.start_players}-{qtd_matches:03d}', stage_id=stage_id)
                self.session.add(match)
                match_detail = MatchDetail(match_id=match.id, title=match.title, participants=[])
                for _ in range(8):
                    shuffle(user_list)
                    user_id = user_list.pop()
                    match_users = MatchUser(match_id=match.id, user_id=user_id)
                    self.session.add(match_users)
                    match_detail.participants.append(user_id)
                match_list.append(match_detail.model_dump())
            return match_list

        except Exception as e:
            raise ControllerException(404, f"Couldnt update stage: {e}")