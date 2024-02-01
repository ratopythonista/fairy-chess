from enum import Enum
from time import sleep

from fastapi import HTTPException
from requests import Session, Response

from fairy_chess.config import RIOT_API_KEY


class Endpoint(str, Enum):
    PUUID           = "https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{}/{}"
    SUMMONER        = "https://br1.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{}"
    RANK            = "https://br1.api.riotgames.com/tft/league/v1/entries/by-summoner/{}"
    LAST_MATCH      = "https://americas.api.riotgames.com/tft/match/v1/matches/by-puuid/{}/ids?start=0&count=1"
    MATCH_DETAILS   = "https://americas.api.riotgames.com/tft/match/v1/matches/{}"


class RiotService():
    def __init__(self) -> None:
        self.session = Session()
        self.session.headers = {"Content-Type": "application/json", "X-Riot-Token": RIOT_API_KEY}
        super().__init__()

    def get_league_points(self, riot_id: str) -> int:
        response: Response = None
        name, tag = riot_id.split("#")
        try:
            from loguru import logger
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

    # def get_last_match(self, puuid: str) -> Match:
    #     response: Response = None
    #     try:
    #         response = self.session.get(Endpoint.LAST_MATCH.format(puuid))
    #         last_match_response: dict = response.json()

    #         response = self.session.get(Endpoint.MATCH_DETAILS.format(last_match_response[0]))
    #         match_detail_response: dict[str, dict[str, list[dict]]] = response.json()

    #         placement_list = [
    #             Placement(map(content.get, ["puuid", "placement"]))
    #             for content in match_detail_response["info"]["participants"]
    #         ]
        
    #         return Match(match_id=last_match_response[0], placement=placement_list)

    #     except Exception as e:
    #         raise HTTPException(500, str(e))
    