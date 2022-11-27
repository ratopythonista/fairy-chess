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
    

def get_tournament_list():
    return [
        {
            "name": "tournament #1",
            "date": "01-01-2017 23:50",
            "summoners":["AB", "AB", "AB", "AB", "AB"]
        },
        {
            "name": "tournament #2",
            "date": "02-01-2017 23:50",
            "summoners":["AB", "AB", "AB", "AB", "AB"]
        },
        {
            "name": "tournament #3",
            "date": "03-01-2017 23:50",
            "summoners":["AB", "AB", "AB", "AB", "AB"]
        }
    ]