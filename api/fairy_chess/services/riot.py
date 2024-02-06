from enum import Enum
from time import sleep

from fastapi import HTTPException
from requests import Session, Response

from fairy_chess.config import RIOT_API_KEY


class Endpoint(str, Enum):
    PUUID           = "https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{}/{}"
    RIOT_ID         = "https://americas.api.riotgames.com/riot/account/v1/accounts/by-puuid/{}"
    SUMMONER        = "https://br1.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{}"
    RANK            = "https://br1.api.riotgames.com/tft/league/v1/entries/by-summoner/{}"
    LAST_MATCH      = "https://americas.api.riotgames.com/tft/match/v1/matches/by-puuid/{}/ids?start=0&count=1"
    MATCH_DETAILS   = "https://americas.api.riotgames.com/tft/match/v1/matches/{}"


class RiotService():
    def __init__(self) -> None:
        self.session = Session()
        self.session.headers = {"Content-Type": "application/json", "X-Riot-Token": RIOT_API_KEY}
        super().__init__()

    def get_riot_id(self, puuid: str) -> str:
        response: Response = None
        try:
            response = self.session.get(Endpoint.RIOT_ID.format(puuid))
            summoner_response: dict = response.json()
            return summoner_response.get("gameName") + "#" + summoner_response.get("tagLine")
        except Exception as e:
            raise HTTPException(500, str(e))

    def get_league_points(self, riot_id: str) -> int:
        response: Response = None
        name, tag = riot_id.split("#")
        try:
            response = self.session.get(Endpoint.PUUID.format(name, tag))
            puuid_response: dict = response.json()
            
            sleep(1)

            response = self.session.get(Endpoint.SUMMONER.format(puuid_response.get("puuid")))
            summoner_response: dict = response.json()

            sleep(1)

            response = self.session.get(Endpoint.RANK.format(summoner_response.get("id")))
            rank_response: list[dict] = response.json()

            sleep(1)

            tier_list = ["IRON", "BRONZE", "SILVER", "GOLD", "PLATINUM", "EMERALD", "DIAMOND", "MASTER", "GRANDMASTER", "CHALLENGER"]
            rank_list = ["I", "II", "III", "IV"]
            for content in rank_response:
                if content.get("queueType") == "RANKED_TFT":
                    tier, rank, lp = map(content.get, ["tier", "rank", "leaguePoints"])
                    if tier == "UNRANKED":
                        lp = 0
                    lp = (tier_list.index(tier) * 4 + rank_list.index(rank)) * 100 + lp
                    return lp

        except Exception as e:
            raise HTTPException(500, str(e))

    def get_last_match(self, riot_id: str) -> dict[str, int]:
        response: Response = None
        name, tag = riot_id.split("#")
        try:
            response = self.session.get(Endpoint.PUUID.format(name, tag))
            puuid_response: dict = response.json()
            
            sleep(1)
        
            response = self.session.get(Endpoint.LAST_MATCH.format(puuid_response.get("puuid")))
            match_response: dict = response.json()

            sleep(1)

            match_riot_id = match_response[0]
            response = self.session.get(Endpoint.MATCH_DETAILS.format(match_riot_id))
            match_detail_response: dict[str, dict[str, list[dict]]] = response.json()

            placement_data = {}
            for content in match_detail_response["info"]["participants"]:
                puuid, placement = map(content.get, ["puuid", "placement"])
                riot_id = self.get_riot_id(puuid)
                placement_data[riot_id] = placement

            return match_riot_id, placement_data

        except Exception as e:
            raise HTTPException(500, str(e))
    