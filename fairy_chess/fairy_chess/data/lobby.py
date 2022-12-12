def sample():
    return {
        "name": "summoner",
        "email": "summoner@email.com",
        "icon": "/foto.jpg",
        "matches": [3,3,4,3,0]
    }

def get_lobby():
    return{
        "summoners": [sample() for _ in range(8)],
        "matches": 5
    }
    