import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

# Create Supabase client with default settings
# The connection pool issue is likely due to HTTP/2 multiplexing in Supabase's httpx client
# This should be handled by Supabase internally
db_client: Client = create_client(url, key)

