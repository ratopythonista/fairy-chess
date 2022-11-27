def sample(index):
    return {
        "name": f"lobby {index}",
        "icon": "/foto.jpg",
        "date": "16-02-2022 23:00",
        "summoners": [{"icon": "/foto.jpg"}, {"icon": "/foto.jpg"}, {"icon": "/foto.jpg"}, {"icon": "/foto.jpg"}, {"icon": "/foto.jpg"}, {"icon": "/foto.jpg"}]
    }

def get_tournament():
    return{
        "lobbies": [sample(index) for index in range(8)],
        "matches": 5
    }
    