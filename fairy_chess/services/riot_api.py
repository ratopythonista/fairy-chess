import requests

from fairy_chess.config import RIOT_API_KEY, RIOT_API_URL


class TFTAPI:
    def __init__(self, summoner_name: str) -> None:
        self.summoner_name = summoner_name
        self.summoners = "tft/summoner/v1/summoners"
        self.league = "tft/league/v1/entries"

    def __request(self, path: str) -> dict:
        headers = {"Content-Type": "application/json", "X-Riot-Token": RIOT_API_KEY}
        return requests.get(f"{RIOT_API_URL}/{path}", headers=headers).json()

    def get_icon(self) -> int:
        return self.__request(f"{self.summoners}/by-name/{self.summoner_name}").get("profileIconId")

    def get_summoner_id(self) -> int:
        return self.__request(f"{self.summoners}/by-name/{self.summoner_name}").get("id")

    def get_ranking(self):
        summoner_id = self.get_summoner_id()
        queue_rank = dict()
        for queue_info in self.__request(f"{self.league}/by-summoner/{summoner_id}"):
            queue_rank[queue_info.get("queueType")] = map(queue_info.get, ['tier', 'rank'])

        if 'RANKED_TFT' in queue_rank:
            return queue_rank['RANKED_TFT']
        return "unranked", ""
