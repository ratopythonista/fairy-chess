import os
from base64 import b64encode
from dataclasses import dataclass

import requests
from riotwatcher import TftWatcher

from fairy_chess.config import RIOT_KEY


@dataclass
class Riot():
    watcher = TftWatcher(RIOT_KEY)
    ddragon = "http://ddragon.leagueoflegends.com/cdn/12.23.1"

    def get_summoner(self, name) -> dict:
        return self.watcher.summoner.by_name("br1", name)


    def get_icon(self, profile_icon_id: int):
        image_name = f"{profile_icon_id}.png"

        # image_data = icon_driver.get(image_name)
        # if image_data:
        #     image_data = image_data.read()
        # else:
        image_data = requests.get(f"{self.ddragon}/img/profileicon/{image_name}").content
            # icon_driver.put(image_name, image_data)
        
        return f"data:image/png;base64, {b64encode(image_data).decode()}"
