import os
from dotenv import load_dotenv

load_dotenv(".env")

PGSQL_URI = os.getenv("PGSQL_URI")
RIOT_API_KEY = os.getenv("RIOT_API_KEY")
HASH_KEY = os.getenv("HASH_KEY")
JWT_KEY = os.getenv("JWT_KEY")


