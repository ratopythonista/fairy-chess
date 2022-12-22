from fairy_chess.services.cache import Cache
from fairy_chess.config import REDIS_EXP_TIME


def login(host_ip: str, user_id: str):
    Cache().put(host_ip, user_id, REDIS_EXP_TIME)


def get_current(host_ip: str):
    return Cache().get(host_ip)


def logout(host_ip: str):
    Cache().delete(host_ip)