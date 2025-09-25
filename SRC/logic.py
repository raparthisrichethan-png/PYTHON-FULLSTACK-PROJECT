# logic.py
from db import create_package, get_packages, update_package, delete_package

# Add a new package
def add_new_package(tracking_number, courier, expected_delivery, origin, destination, notes=""):
    return create_package(
        tracking_number=tracking_number,
        courier=courier,
        status="Pending",  # default
        expected_delivery=expected_delivery,
        origin=origin,
        destination=destination,
        notes=notes
    )

# List all packages
def list_all_packages():
    response = get_packages()
    return response.data if response and hasattr(response, "data") else []

# Find package by ID
def get_package_by_id(package_id):
    packages = list_all_packages()
    for pkg in packages:
        if pkg["id"] == package_id:
            return pkg
    return None

# Update package status
def update_package_status(package_id, status, notes=None):
    updates = {"status": status}
    if notes:
        updates["notes"] = notes
    return update_package(package_id, updates)

# Remove package
def remove_package(package_id):
    return delete_package(package_id)

# Search by tracking number
def find_package_by_tracking(tracking_number):
    packages = list_all_packages()
    for pkg in packages:
        if pkg["tracking_number"] == tracking_number:
            return pkg
    return None
