import streamlit as st
import requests

BASE_URL = "http://127.0.0.1:8000"

st.title("Package Delivery Tracker")

# Add Package Form
with st.form("add_package"):
    tracking_number = st.text_input("Tracking Number")
    courier = st.text_input("Courier")
    status = st.text_input("Status")
    origin = st.text_input("Origin")
    destination = st.text_input("Destination")
    expected_delivery = st.date_input("Expected Delivery")
    notes = st.text_area("Notes")
    submitted = st.form_submit_button("Add Package")
    
    if submitted:
        payload = {
            "tracking_number": tracking_number,
            "courier": courier,
            "status": status,
            "origin": origin,
            "destination": destination,
            "expected_delivery": str(expected_delivery),
            "notes": notes
        }
        response = requests.post(f"{BASE_URL}/packages/", json=payload)
        st.write(response.json())

# Show All Packages
if st.button("Show Packages"):
    response = requests.get(f"{BASE_URL}/packages/")
    st.write(response.json())
