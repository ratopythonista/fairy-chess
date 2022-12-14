from uuid import uuid4

from jose import jwe

from fairy_chess.config import API_KEY
from fairy_chess.data import user_base

def put(name: str, email: str, password: str, user_id=str(uuid4())):
    user_base.put(
        {
            "email": email,
            "name": name,
            "password": jwe.encrypt(password, API_KEY, algorithm='dir', encryption='A128GCM').decode()
        },
        key=user_id
    )
    

def authenticate(email: str, password: str):
    user_dict: dict = user_base.fetch({"email": email}).items
    if user_dict:
        user_dict = user_dict[0]
        password_stored = jwe.decrypt(user_dict.get("password"), API_KEY).decode()
        if password == password_stored:
            return user_dict.get("key")