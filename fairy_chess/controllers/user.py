from loguru import logger

from fairy_chess.services.riot import RiotClient
from fairy_chess.services.supabase_service import supabase

from gotrue.errors import AuthApiError

class UserController:

    def register(email: str, password: str, summoner_name: str):
        try:
            summoner_puuid = RiotClient().get_puuid(summoner_name)
            data = supabase.auth.sign_up({
                "email": email,
                "password": password,
                "options": {
                    "data": {
                        "summoner_puuid": summoner_puuid,
                        "validated": False
                    }
                }
            })
            return data
        except AuthApiError as err:
            logger.error(f"Error registering user {email}:  {err.message}")

    def login(email: str, password: str):
        data = supabase.auth.sign_in_with_password({"email": email, "password": password})
        
        riot_client = RiotClient()
        
        summoner_data = riot_client.get_summoner_by_puuid(data.user.user_metadata.get("summoner_puuid"))
        
        
        
        summoner = summoner_data.get("name")
        validated = data.user.user_metadata.get("validated")
        icon = riot_client.get_icon(summoner_data.get("profileIconId"))
        
        logger.info(icon)
        return summoner, validated, icon


