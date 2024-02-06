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
    
    def init_lobby(self, title: str, stage_id: str, competitors: list[StageUser]) -> list[LobbyUser]:
        return LobbyRepository().init_lobby(title, stage_id, competitors)