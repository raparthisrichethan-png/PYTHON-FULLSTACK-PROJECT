# db_manager.py
import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(url, key)

# Create a new package
def create_package(tracking_number, courier, status, expected_delivery, origin, destination, notes):
    return supabase.table("packages").insert({
        "tracking_number": tracking_number,
        "courier": courier,
        "status": status,
        "expected_delivery": expected_delivery,
        "origin": origin,
        "destination": destination,
        "notes": notes
    }).execute()

# Get all packages
def get_packages():
    return supabase.table("packages").select("*").execute()

# Update a package (flexible)
def update_package(id, updates):
    return supabase.table("packages").update(updates).eq("id", id).execute()

# Delete a package
def delete_package(id):
    return supabase.table("packages").delete().eq("id", id).execute()
