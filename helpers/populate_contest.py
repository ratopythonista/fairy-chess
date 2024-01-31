import requests
from time import sleep

REGISTER_URL = "http://localhost:8000/api/v1/user/register"
LINK_RIOT_URL = "http://localhost:8000/api/v1/user/link/riot?riot_id={}"
CONTEST_URL = "http://localhost:8000/api/v1/contest/register/70d5ec57-64d3-42ce-b6f9-e5729d2ea074"

riot_id_list = open("riot_id_list.txt").read().split("\n")

for index, riot_id in riot_id_list:
    body = {
        "email": f"teste{index}@fairy.chess",
        "password": "12345678",
    }
    response: dict = requests.post(REGISTER_URL, json=body).json()
    header = {"X-Token": response.get("access_token")}
    requests.post(LINK_RIOT_URL.format(riot_id), headers=header).json()
    requests.post(CONTEST_URL, headers=header).json()
    print(body.get("email"))
