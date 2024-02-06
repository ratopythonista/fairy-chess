from fairy_chess.database.models.user import UserRepository
from fairy_chess.database.models.lobby import LobbyRepository
from fairy_chess.database.models.match import MatchRepository, MatchUser

class MatchController:    
    def init_match(self, title: str, match_riot_id: str, lobby_id: str, placement_data: dict[str, int]) -> list[MatchUser]:
        placements = placement_data.values()

        # user_repository = UserRepository()
        # competitors = [user_repository.find_by_riot_id(riot_id=riot_id).id for riot_id in placement_data.keys()] # COMMENT WHILE TESTING
        competitors = [user.user_id for user in LobbyRepository().competitors(lobby_id=lobby_id)] # ONLY FOR TEST PROPOUSE

        return MatchRepository().init_match(title, match_riot_id, lobby_id, competitors, placements)