from fairy_chess.services.riot import RiotService

from fairy_chess.controllers.match import MatchController

from fairy_chess.database.models.user import UserRepository
from fairy_chess.database.models.lobby import LobbyRepository, StageUser, LobbyUser


class LobbyController:
    def fetch(self, stage_id: str) -> list[dict]:
        formated_response, lobby_repository = list(), LobbyRepository()
        for lobby in lobby_repository.fetch_by_stage_id(stage_id):
            formated_response.append({
                "lobby": lobby.model_dump(exclude={'stage_id'}),
                "competitors": [
                    competitor.model_dump(exclude={'lobby_id', 'check_in'})
                    for competitor in lobby_repository.competitors(lobby_id=lobby.id)
                ]
            })

        return formated_response
    

    def create_match(self, lobby_id: str, match_index: int, user_id: str) -> list[dict]:
        user_repository = UserRepository()

        riot_id = user_repository.find_by_id(user_id=user_id).riot_id
        match_riot_id, placement_data = RiotService().get_last_match(riot_id=riot_id)

        return MatchController().init_match(
            title=f"Match {match_index}",
            match_riot_id=match_riot_id,
            lobby_id=lobby_id,
            placement_data=placement_data
        )
    
    def init_lobby(self, title: str, stage_id: str, competitors: list[StageUser]) -> list[LobbyUser]:
        return LobbyRepository().init_lobby(title, stage_id, competitors)