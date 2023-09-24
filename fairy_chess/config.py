import os
from dotenv import load_dotenv

load_dotenv(".env")

DATABSE_URI = os.getenv("DATABASE_URI")
RIOT_API_KEY = os.getenv("RIOT_API_KEY")