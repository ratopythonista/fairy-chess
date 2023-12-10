import requests

from fairy_chess.config import RIOT_API_KEY

RANK_PATH = "https://br1.api.riotgames.com/tft/league/v1/entries/by-summoner"
PUUID_PATH = "https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id"
TFT_SUMMONER_PATH = "https://br1.api.riotgames.com/tft/summoner/v1/summoners/by-puuid"

class Riot:
    def __init__(self, riot_id: str) -> None:
        self.riot_id = riot_id

    def __request(self, path: str) -> dict:
        headers = {"Content-Type": "application/json", "X-Riot-Token": RIOT_API_KEY}
        return requests.get(path, headers=headers).json()

    @property
    def puuid(self) -> int:
        game_name, tag_line = self.riot_id.split("#")
        response: dict = self.__request(f"{PUUID_PATH}/{game_name}/{tag_line}")
        return response.get("puuid")
   
    @property
    def icon(self):
        response: dict = self.__request(f"{TFT_SUMMONER_PATH}/{self.puuid}")
        icon_id, self.summoner_id = map(response.get, ["profileIconId", "id"])
        return icon_id

    @property
    def rank(self):
        response: list[dict] = self.__request(f"{RANK_PATH}/{self.summoner_id}")
        tft_ranked = {"tier": "Unranked", "rank": ""}
        for rank in response:
            if rank.get("queueType"):
                tft_ranked = rank
        return ' '.join(map(tft_ranked.get, ["tier", "rank"]))
