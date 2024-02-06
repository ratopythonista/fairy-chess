from random import shuffle as shuffle_list

from fairy_chess.exceptions import ControllerException

from fairy_chess.controllers.lobby import LobbyController

from fairy_chess.database.models.lobby import LobbyRepository, LobbyUser
from fairy_chess.database.models.contest import ContestRepository, Contest
from fairy_chess.database.models.stage import StageRepository, Contest, StageUser, Stage


class StageController:
    def __insert_stage_user(self, stage_id: str, user_id: str) -> StageUser:
        stage_user = StageUser(stage_id=stage_id, user_id=user_id)
        self.session.add(stage_user)
        self.session.commit()
        self.session.refresh(stage_user)
        return stage_user
    
    def __check_ownership(self, stage_id: str, user_id: str):
        stage: Stage = StageRepository().fetch_one(stage_id)
        if not stage:
            raise ControllerException(404, f"The contest {stage_id} does not exist")
        contest: Contest = ContestRepository().find_by_id(contest_id=stage.contest_id)
        if contest['creator'] != user_id:
            raise ControllerException(403, f"Only the creator can start the stage")

    def fetch(self, contest_id: str) -> list[dict]:
        return [stage.model_dump() for stage in StageRepository().fetch_by_contest_id(contest_id)]
    
    def shuffle(self, stage_id: str, round: int, user_id: str):
        self.__check_ownership(stage_id, user_id)
        competitors = StageRepository().competitors(stage_id)
        shuffle_list(competitors)
        lobbies, lobby_letter = list(), 'A'
        for index in range(0, len(competitors)-7, 8):
            lobby_competitors = competitors[index:index+8]
            lobby_info = LobbyController().init_lobby(title=f'LOBBY {round}-{lobby_letter}', stage_id=stage_id, competitors=lobby_competitors)
            lobbies.append([competitors.model_dump(exclude={'check_in', 'lobby_id'}) for competitors in lobby_info])
            lobby_letter = chr(ord(lobby_letter) + 1)
        return lobbies

    def start(self, stage_id: str, user_id: str):
        self.__check_ownership(stage_id, user_id)
        competitors = StageRepository().competitors(stage_id)
        lobby_list: list[list[LobbyUser]] = []
        for index in range(0, len(competitors), 8):
            LobbyRepository().init_lobby(title=f'LOBBY {index}', stage_id=stage_id)
            lobby_list.append(self.__insert_stage_user(stage_id, competitors[index].user_id))
        return lobby_list


