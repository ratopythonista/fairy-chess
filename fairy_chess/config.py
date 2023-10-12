import os
from dotenv import load_dotenv

load_dotenv(".env")

HASH_KEY = os.getenv("HASH_KEY")
DATABSE_URI = os.getenv("DATABASE_URI")
RIOT_API_KEY = os.getenv("RIOT_API_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")


