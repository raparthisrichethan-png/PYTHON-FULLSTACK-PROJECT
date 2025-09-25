# app.py
import streamlit as st
from logic import add_new_package, list_all_packages, update_package_status, remove_package, find_package_by_tracking

st.set_page_config(page_title="📦 Package Delivery Tracker", layout="wide")

st.title("📦 Package Delivery Tracker")

menu = st.sidebar.radio("Menu", ["Add Package", "View Packages", "Update Status", "Delete Package", "Search Package"])

# Add Package
if menu == "Add Package":
    st.subheader("➕ Add a New Package")
    tracking_number = st.text_input("Tracking Number")
    courier = st.text_input("Courier")
    expected_delivery = st.date_input("Expected Delivery")
    origin = st.text_input("Origin")
    destination = st.text_input("Destination")
    notes = st.text_area("Notes")

    if st.button("Add Package"):
        add_new_package(tracking_number, courier, str(expected_delivery), origin, destination, notes)
        st.success("✅ Package added successfully!")

# View Packages
elif menu == "View Packages":
    st.subheader("📋 All Packages")
    packages = list_all_packages()
    if packages:
        st.dataframe(packages)
    else:
        st.info("No packages found.")

# Update Status
elif menu == "Update Status":
    st.subheader("✏️ Update Package Status")
    package_id = st.number_input("Enter Package ID", min_value=1, step=1)
    new_status = st.selectbox("Select New Status", ["Pending", "In Transit", "Out for Delivery", "Delivered", "Delayed"])
    notes = st.text_area("Notes (optional)")

    if st.button("Update"):
        update_package_status(package_id, new_status, notes)
        st.success("✅ Package updated successfully!")

# Delete Package
elif menu == "Delete Package":
    st.subheader("🗑️ Delete Package")
    package_id = st.number_input("Enter Package ID to Delete", min_value=1, step=1)

    if st.button("Delete"):
        remove_package(package_id)
        st.success("✅ Package deleted successfully!")

# Search Package
elif menu == "Search Package":
    st.subheader("🔍 Search by Tracking Number")
    tracking_number = st.text_input("Enter Tracking Number")

    if st.button("Search"):
        result = find_package_by_tracking(tracking_number)
        if result:
            st.json(result)
        else:
            st.warning("❌ No package found with this tracking number.")
