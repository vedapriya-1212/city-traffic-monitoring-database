from supabase import create_client, Client
import os
from dotenv import load_dotenv

load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

def get_supabase() -> Client:
    if not url or not key:
        raise Exception("Supabase URL or KEY not found in environment")
    return create_client(url, key)

