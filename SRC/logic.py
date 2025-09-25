from SRC.db import DatabaseManager

class PackageManager:
    """Acts as a bridge b/w frontend(streamlit/fastapi) and the database."""
    
    def __init__(self):
        self.db = DatabaseManager()

    def add_package(self, tracking_number, courier, status, expected_delivery, origin, destination, notes):
        if not tracking_number or not courier:
            return {"error": "Tracking number and courier are required."}
        
        result = self.db.create_package(tracking_number, courier, status, expected_delivery, origin, destination, notes)
        if result.get("error"):
            return {"error": result["error"]}
        
        return {"success": "Package added successfully."}

    def get_all_packages(self):
        return self.db.get_packages()

    def update_package(self, id, updates):
        return self.db.update_package(id, updates)

    def delete_package(self, id):
        return self.db.delete_package(id)
