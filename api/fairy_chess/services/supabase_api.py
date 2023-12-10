from supabase import create_client, Client
from loguru import logger
from fairy_chess.config import SUPABASE_KEY, SUPABASE_URL


class SupabaseAPI:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    def __init__(self, bucket: str = 'develop') -> None:
        self.bucket: str = bucket
        
    def get_icon(self, icon_id: int):
        return SupabaseAPI.supabase.storage.from_(self.bucket).get_public_url(f'riot/icon/{icon_id}.png')
    
    def get_rank_icon(self, rank_name: str):
        return SupabaseAPI.supabase.storage.from_(self.bucket).get_public_url(f'riot/rank/{rank_name}.png')

    def create_user(self, email: str, password: str, summoner_name: str) -> None:
        logger.debug(email)
        return self.supabase.auth.sign_up({
            "email": email,
            "password": password,
            "options": {
                "data": {
                    "summoner_name": summoner_name
                }
            }
        }).session.access_token

    def login(self, email: str, password: str) -> None:
        return SupabaseAPI.supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        }).session.access_token
        
    
    def get_current_user(self) -> None:
        data = SupabaseAPI.supabase.auth.get_user()
        return data.user.user_metadata.get("summoner_name")