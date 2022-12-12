import os
from random import randint

from riotwatcher import TftWatcher


RIOT_KEY = os.getenv("RIOT_KEY")

def get_summoner(name) -> dict:
    return TftWatcher(RIOT_KEY).summoner.by_name("br1", name)


def get_icon(puuid):
    user: dict = TftWatcher(RIOT_KEY).summoner.by_puuid("br1", puuid)
    return f"http://ddragon.leagueoflegends.com/cdn/12.23.1/img/profileicon/{user.get('profileIconId')}.png"