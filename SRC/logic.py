from SRC.db import DatabaseManager
from datetime import date
import re

class PackageManager:
    """Bridge between frontend and database with business logic validation."""

    def __init__(self):
        self.db = DatabaseManager()

    def _validate_tracking_number(self, tracking_number):
        """Validate tracking number format."""
        if not tracking_number or len(tracking_number.strip()) == 0:
            return False, "Tracking number cannot be empty"
        if len(tracking_number) > 50:
            return False, "Tracking number too long (max 50 characters)"
        return True, None

    def _validate_courier(self, courier):
        """Validate courier name."""
        if not courier or len(courier.strip()) == 0:
            return False, "Courier name cannot be empty"
        if len(courier) > 100:
            return False, "Courier name too long (max 100 characters)"
        return True, None

    def add_package(self, tracking_number, courier, status, expected_delivery, origin, destination, notes=None):
        """Add a new package with validation."""
        # Validate inputs
        is_valid, error = self._validate_tracking_number(tracking_number)
        if not is_valid:
            return {"success": False, "error": error}
        
        is_valid, error = self._validate_courier(courier)
        if not is_valid:
            return {"success": False, "error": error}

        # Convert date if needed
        if isinstance(expected_delivery, date):
            expected_delivery = expected_delivery.isoformat()

        # Check for duplicate tracking numbers
        existing = self.db.search_packages(tracking_number=tracking_number)
        if existing.get("success") and existing.get("data"):
            return {"success": False, "error": "Tracking number already exists"}

        result = self.db.create_package(
            tracking_number.strip(),
            courier.strip(),
            status,
            expected_delivery,
            origin,
            destination,
            notes
        )
        return result

    def get_all_packages(self, limit=100, offset=0):
        """Retrieve all packages with pagination."""
        return self.db.get_packages(limit=limit, offset=offset)

    def get_package(self, id):
        """Get a single package by ID."""
        return self.db.get_package_by_id(id)

    def search_packages(self, tracking_number=None, courier=None, status=None):
        """Search packages by criteria."""
        return self.db.search_packages(tracking_number, courier, status)

    def update_package(self, id, updates: dict):
        """Update package with validation."""
        if not updates:
            return {"success": False, "error": "No updates provided"}

        # Validate tracking number if being updated
        if "tracking_number" in updates:
            is_valid, error = self._validate_tracking_number(updates["tracking_number"])
            if not is_valid:
                return {"success": False, "error": error}
            updates["tracking_number"] = updates["tracking_number"].strip()

        # Validate courier if being updated
        if "courier" in updates:
            is_valid, error = self._validate_courier(updates["courier"])
            if not is_valid:
                return {"success": False, "error": error}
            updates["courier"] = updates["courier"].strip()

        # Convert date if needed
        if "expected_delivery" in updates and isinstance(updates["expected_delivery"], date):
            updates["expected_delivery"] = updates["expected_delivery"].isoformat()

        return self.db.update_package(id, updates)

    def delete_package(self, id):
        """Delete a package by ID."""
        return self.db.delete_package(id)