from riotwatcher import LolWatcher

from config import RIOT_API_KEY


class RiotClient:
    def __init__(self) -> None:
        self.lol_watcher = LolWatcher(RIOT_API_KEY)
        self.my_region = 'br1'

    def get_puuid(self, summoner_name: str):
        user: dict = self.lol_watcher.summoner.by_name(self.my_region, summoner_name)
        return user.get('puuid')
    
