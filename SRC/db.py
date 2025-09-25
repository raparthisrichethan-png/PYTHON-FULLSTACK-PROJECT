# db_manager.py
import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(url, key)

class DatabaseManager:
    def __init__(self):
        self.supabase = supabase

    # Create a new package
    def create_package(self, tracking_number, courier, status, expected_delivery, origin, destination, notes):
        return self.supabase.table("packages").insert({
            "tracking_number": tracking_number,
            "courier": courier,
            "status": status,
            "expected_delivery": expected_delivery,
            "origin": origin,
            "destination": destination,
            "notes": notes
        }).execute()

    # Get all packages
    def get_packages(self):
        return self.supabase.table("packages").select("*").execute()

    # Update a package (flexible)
    def update_package(self, id, updates):
        return self.supabase.table("packages").update(updates).eq("id", id).execute()

    # Delete a package
    def delete_package(self, id):
        return self.supabase.table("packages").delete().eq("id", id).execute()
