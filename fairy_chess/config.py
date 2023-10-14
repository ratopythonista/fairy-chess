import os
from dotenv import load_dotenv

load_dotenv(".env")

RIOT_API_URL = os.getenv("RIOT_API_URL")
RIOT_API_KEY = os.getenv("RIOT_API_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")


