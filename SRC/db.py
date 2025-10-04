import os
from supabase import create_client, Client
from dotenv import load_dotenv
from datetime import date
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseManager:
    """Manages all database operations with Supabase."""
    
    def __init__(self):
        load_dotenv()
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_KEY")
        
        if not url or not key:
            raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in environment variables")
        
        self.supabase: Client = create_client(url, key)
        logger.info("Database connection established")

    def create_package(self, tracking_number, courier, status, expected_delivery, origin, destination, notes=None):
        """Create a new package in the database."""
        try:
            if isinstance(expected_delivery, date):
                expected_delivery = expected_delivery.isoformat()
            
            response = self.supabase.table("packages").insert({
                "tracking_number": tracking_number,
                "courier": courier,
                "status": status,
                "expected_delivery": expected_delivery,
                "origin": origin,
                "destination": destination,
                "notes": notes
            }).execute()
            
            logger.info(f"Package created: {tracking_number}")
            return {"success": True, "data": response.data[0]}
        except Exception as e:
            logger.error(f"Error creating package: {str(e)}")
            return {"success": False, "error": str(e)}

    def get_packages(self, limit=100, offset=0):
        """Retrieve all packages with optional pagination."""
        try:
            response = (
                self.supabase.table("packages")
                .select("*")
                .order("id", desc=True)
                .limit(limit)
                .offset(offset)
                .execute()
            )
            return {"success": True, "data": response.data}
        except Exception as e:
            logger.error(f"Error fetching packages: {str(e)}")
            return {"success": False, "error": str(e)}

    def get_package_by_id(self, id):
        """Retrieve a single package by ID."""
        try:
            response = (
                self.supabase.table("packages")
                .select("*")
                .eq("id", id)
                .execute()
            )
            if response.data:
                return {"success": True, "data": response.data[0]}
            return {"success": False, "error": "Package not found"}
        except Exception as e:
            logger.error(f"Error fetching package {id}: {str(e)}")
            return {"success": False, "error": str(e)}

    def search_packages(self, tracking_number=None, courier=None, status=None):
        """Search packages by various criteria."""
        try:
            query = self.supabase.table("packages").select("*")
            
            if tracking_number:
                query = query.ilike("tracking_number", f"%{tracking_number}%")
            if courier:
                query = query.ilike("courier", f"%{courier}%")
            if status:
                query = query.eq("status", status)
            
            response = query.order("id", desc=True).execute()
            return {"success": True, "data": response.data}
        except Exception as e:
            logger.error(f"Error searching packages: {str(e)}")
            return {"success": False, "error": str(e)}

    def update_package(self, id, updates):
        """Update an existing package."""
        try:
            if "expected_delivery" in updates and isinstance(updates["expected_delivery"], date):
                updates["expected_delivery"] = updates["expected_delivery"].isoformat()
            
            response = (
                self.supabase.table("packages")
                .update(updates)
                .eq("id", id)
                .execute()
            )
            
            if response.data:
                logger.info(f"Package {id} updated")
                return {"success": True, "data": response.data[0]}
            return {"success": False, "error": "Package not found"}
        except Exception as e:
            logger.error(f"Error updating package {id}: {str(e)}")
            return {"success": False, "error": str(e)}

    def delete_package(self, id):
        """Delete a package by ID."""
        try:
            response = (
                self.supabase.table("packages")
                .delete()
                .eq("id", id)
                .execute()
            )
            
            if response.data:
                logger.info(f"Package {id} deleted")
                return {"success": True, "message": f"Package {id} deleted"}
            return {"success": False, "error": "Package not found"}
        except Exception as e:
            logger.error(f"Error deleting package {id}: {str(e)}")
            return {"success": False, "error": str(e)}