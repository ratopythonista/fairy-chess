import requests
from riotwatcher import LolWatcher


from config import RIOT_API_KEY


class RiotClient:
    def __init__(self, version="13.20.1") -> None:
        self.lol_watcher = LolWatcher(RIOT_API_KEY)
        self.my_region = 'br1'
        self.data_dragon_icon_path = f"http://ddragon.leagueoflegends.com/cdn/{version}/img/profileicon/"

    def get_puuid(self, summoner_name: str):
        user: dict = self.lol_watcher.summoner.by_name(self.my_region, summoner_name)
        return user.get('puuid')
    
    def get_summoner_by_puuid(self, puuid: str):
        user: dict = self.lol_watcher.summoner.by_puuid(self.my_region, puuid)
        return user
    
    def get_icon(self, icon_id: int):
        return f"{self.data_dragon_icon_path}{icon_id}.png"
