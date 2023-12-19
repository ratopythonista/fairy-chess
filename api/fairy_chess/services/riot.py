from enum import StrEnum

from requests import Session, Response
from fastapi import HTTPException
from pydantic import BaseModel, Field

from fairy_chess.config import RIOT_API_KEY


class Endpoint(StrEnum):
    PUUID           = "https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{}/{}"
    SUMMONER        = "https://br1.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{}"
    RANK            = "https://br1.api.riotgames.com/tft/league/v1/entries/by-summoner/{}"
    LAST_MATCH      = "https://americas.api.riotgames.com/tft/match/v1/matches/by-puuid/{}/ids?start=0&count=1"
    MATCH_DETAILS   = "https://americas.api.riotgames.com/tft/match/v1/matches/{}"


class RiotId(BaseModel):
    name: str = Field(..., description="Riot game name")
    tag: str = Field(..., description="Riot tag")

    def get(self) -> str:
        return f"{self.name}#{self.tag}"
    
class TFTRank(BaseModel):
    tier: str = Field("Unranked", description="TFT Ranked Tier")
    rank: str = Field("", description="TFT Ranked Rank")

    def get(self) -> str:
        return f"{self.tier} {self.rank}"
    
class Placement(BaseModel):
    puuid: str = Field(..., description="Public User ID")
    placement: int = Field("", description="TFT Ranked Rank")


class Summoner(BaseModel):
    summoner_id: str = Field(..., description="Riot Summoner ID")
    puuid: str = Field(..., description="Public User ID")
    icon_id: int = Field(..., description="Icon ID")
    riot_id: RiotId = Field(..., description="Riot ID")
    tft_rank: TFTRank = Field(..., description="TFT Rank")

class Match(BaseModel):
    match_id: str = Field(..., description="Riot Match ID")
    placement: list[Placement] = Field(..., description="Placement for this match")


class RiotService():
    def __init__(self) -> None:
        self.session = Session()
        self.session.headers = {"Content-Type": "application/json", "X-Riot-Token": RIOT_API_KEY}
        super().__init__()

    def get_summoner(self, riot_id: RiotId) -> Summoner:
        from loguru import logger
        response: Response = None
        try:
            response = self.session.get(Endpoint.PUUID.format(riot_id.name, riot_id.tag))
            puuid_response: dict = response.json()

            logger.debug(puuid_response)
            response = self.session.get(Endpoint.SUMMONER.format(puuid_response.get("puuid")))
            summoner_response: dict = response.json()

            logger.debug(summoner_response)
            response = self.session.get(Endpoint.RANK.format(summoner_response.get("id")))
            tft_rank: TFTRank = TFTRank()

            content: dict
            for content in response.json():
                if content.get("queueType") == "RANKED_TFT":
                    tier, rank = map(content.get, ["tier", "rank"])
                    tft_rank = TFTRank(tier=tier, rank=rank)
                    break

            logger.debug(tft_rank)

            return Summoner(
                puuid=puuid_response.get("puuid"),
                icon_id=summoner_response.get("profileIconId"),
                summoner_id=summoner_response.get("id"),
                tft_rank=tft_rank,
                riot_id=riot_id
            )

        except Exception as e:
            raise HTTPException(500, str(e))

    def get_last_match(self, puuid: str) -> Match:
        response: Response = None
        try:
            response = self.session.get(Endpoint.LAST_MATCH.format(puuid))
            last_match_response: dict = response.json()

            response = self.session.get(Endpoint.MATCH_DETAILS.format(last_match_response[0]))
            match_detail_response: dict[str, dict[str, list[dict]]] = response.json()

            placement_list = [
                Placement(map(content.get, ["puuid", "placement"]))
                for content in match_detail_response["info"]["participants"]
            ]
        
            return Match(match_id=last_match_response[0], placement=placement_list)

        except Exception as e:
            raise HTTPException(500, str(e))
    