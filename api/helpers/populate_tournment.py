import requests

REGISTER_URL = "http://localhost:8000/api/v1/user/register"
TOURNMENT_URL = "http://localhost:8000/api/v1/tournemt/register/6581c005f75073621aed7aa4"

with open('competitors', 'r') as file:
    for index, riot_id in enumerate(file.read().split("\n")):
        print(riot_id)
        body = {
            "email": f"teste{index}@fairy.chess",
            "password": "12345678",
            "riot_id": riot_id
        }
        response: dict = requests.post(REGISTER_URL, json=body).json()
        header = {"X-Token": response.get("access_token")}
        response = requests.post(TOURNMENT_URL, json=body, headers=header).json()
        print(len(response.get("competitors")), response.get("competitors"))


    