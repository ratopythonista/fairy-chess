from redis import Redis

from fairy_chess.config import REDIS_HOST

class Cache():
    def __init__(self) -> None:
        self.redis = Redis(host=REDIS_HOST, port=6379, db=0)

    def put(self, key, value, expiration):
        self.redis.set(key, value, ex=expiration,)

    def get(self, key):
        return self.redis.get(key)
    
    def delete(self, key):
        return self.redis.delete(key)