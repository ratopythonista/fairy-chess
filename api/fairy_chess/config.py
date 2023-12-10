import os
from dotenv import load_dotenv

load_dotenv(".env")

MONGO_URI = os.getenv("MONGO_URI")
RIOT_API_KEY = os.getenv("RIOT_API_KEY")


