from loguru import logger

from fairy_chess.services.riot_api import TFTAPI
from fairy_chess.services.supabase_api import SupabaseAPI

from fairy_chess.database.user import RiotUser, User

from gotrue.errors import AuthApiError

class UserController:
    supabase: SupabaseAPI = SupabaseAPI()

    def register(self, user: User):
        try:
            return UserController.supabase.create_user(user.email, user.password, user.summoner_name)
        except AuthApiError as err:
            logger.error(f"Error registering user {user.email}:  {err.message}")

    def login(self, user: User):
        return UserController.supabase.login(user.email, user.password)


    def get_summoner_data(self) -> RiotUser:
        summoner_name = UserController.supabase.get_current_user()
        tft_api = TFTAPI(summoner_name)
        icon_id = tft_api.get_icon()
        rank, tier = tft_api.get_ranking()
        icon_url = UserController.supabase.get_icon(icon_id)
        rank_icon_url = UserController.supabase.get_rank_icon(rank)
        return RiotUser(summoner_name=summoner_name, icon=icon_url, rank=f"{rank} {tier}", rank_icon=rank_icon_url)
