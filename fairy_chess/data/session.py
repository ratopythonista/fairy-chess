from datetime import datetime, timedelta

from fairy_chess.data import session_base

def login(host_ip: str, user_id: str):
    session_base.put(
        data=user_id,
        expire_at=datetime.now() + timedelta(minutes=30),
        key=host_ip
    )

def get_current(host_ip: str):
    return session_base.get(host_ip)


def logout(host_ip: str):
    session_base.delete(host_ip)