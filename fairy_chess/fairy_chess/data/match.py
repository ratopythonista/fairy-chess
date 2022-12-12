def sample():
    return {
        "name": "summoner",
        "email": "summoner@email.com",
        "icon": "/foto.jpg",
        "augments": ["/foto.jpg", "/foto.jpg", "/foto.jpg"],
        "champions": ["/foto.jpg", "/foto.jpg", "/foto.jpg", "/foto.jpg", "/foto.jpg", "/foto.jpg"]
    }

def get_matches():
    return {
        "summoners": [sample() for _ in range(8)]
    }