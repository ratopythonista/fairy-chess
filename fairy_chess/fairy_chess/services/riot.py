import os
from base64 import b64encode
from dataclasses import dataclass

import requests
from riotwatcher import TftWatcher

from fairy_chess.data import icon_driver

RIOT_KEY = os.getenv("RIOT_KEY")
@dataclass
class Riot():
    watcher = TftWatcher(RIOT_KEY)
    ddragon = "http://ddragon.leagueoflegends.com/cdn/12.23.1"

    def get_summoner(self, name) -> dict:
        return self.watcher.summoner.by_name("br1", name)


    def get_icon(self, puuid):
        user: dict = self.watcher.summoner.by_puuid("br1", puuid)
        image_name = f"{user.get('profileIconId')}.png"

        image_data = icon_driver.get(image_name)
        if image_data:
            image_data = image_data.read()
        else:
            image_data = requests.get(f"{self.ddragon}/img/profileicon/{image_name}").content
            icon_driver.put(image_name, image_data)
        
        return b64encode(image_data).decode()
