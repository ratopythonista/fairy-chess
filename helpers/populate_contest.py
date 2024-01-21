import requests
from time import sleep

REGISTER_URL = "http://localhost:8000/api/v1/user/login"
CONTEST_URL = "http://localhost:8000/api/v1/contest/register/70d5ec57-64d3-42ce-b6f9-e5729d2ea074"


for index in range(128):
    body = {
        "email": f"teste{index}@fairy.chess",
        "password": "12345678",
    }
    response: dict = requests.post(REGISTER_URL, json=body).json()
    header = {"X-Token": response.get("access_token")}
    response = requests.post(CONTEST_URL, json=body, headers=header).json()
    print(body.get("email"))
