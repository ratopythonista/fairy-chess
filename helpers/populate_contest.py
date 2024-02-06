import requests
from time import sleep

REGISTER_URL = "http://localhost:8000/api/v1/user/register"
LOGIN_URL = "http://localhost:8000/api/v1/user/login"
LINK_RIOT_URL = "http://localhost:8000/api/v1/user/link/riot?riot_id={}"
CONTEST_URL = "http://localhost:8000/api/v1/contest/register/da043f69-1dde-4122-9dd1-f31c8073b37c"
CONTEST_CHECK_IN_URL = "http://localhost:8000/api/v1/contest/checkin/da043f69-1dde-4122-9dd1-f31c8073b37c"

riot_id_list = open("riot_id_list.txt").read().split("\n")

for index, riot_id in enumerate(riot_id_list):
    print("*"*100)
    print(riot_id, index)
    body = {
        "email": f"teste{index}@fairy.chess",
        "password": "12345678",
    }
    response: dict = requests.post(LOGIN_URL, json=body).json()
    header = {"X-Token": response.get("access_token")}
    # print("REGISTER USER")
    response = requests.post(LINK_RIOT_URL.format(riot_id.replace("#", "%23")), headers=header).json()
    print("REGISTER WITH RIOT")
    # requests.post(CONTEST_URL, headers=header).json()
    # print("REGISTER IN CONTEST")
    # requests.post(CONTEST_CHECK_IN_URL, headers=header).json()
    # print("CHECK IN CONTEST")
    
