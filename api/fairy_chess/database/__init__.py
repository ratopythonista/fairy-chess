from pymongo import MongoClient

from fairy_chess.config import MONGO_URI

client = MongoClient(MONGO_URI)
database = client['FairyChessV1']