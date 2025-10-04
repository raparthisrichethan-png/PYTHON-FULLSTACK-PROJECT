import streamlit as st
import requests
import pandas as pd
from datetime import date, datetime

BASE_URL = "http://127.0.0.1:8000"

# Page config
st.set_page_config(
    page_title="Package Delivery Tracker",
    page_icon="📦",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .stAlert > div {
        padding: 0.5rem 1rem;
    }
    .status-badge {
        padding: 0.25rem 0.5rem;
        border-radius: 0.25rem;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

st.title("📦 Package Delivery Tracker")

# Helper function for API calls
def api_request(method, endpoint, **kwargs):
    """Make API request with error handling."""
    try:
        url = f"{BASE_URL}{endpoint}"
        response = requests.request(method, url, **kwargs)
        
        if response.headers.get("content-type", "").startswith("application/json"):
            data = response.json()
            if response.status_code in [200, 201]:
                return data, None
            else:
                return None, data.get("detail", "Unknown error")
        else:
            return None, f"Non-JSON response: {response.text[:100]}"
    except requests.exceptions.ConnectionError:
        return None, "Could not connect to API. Is the server running?"
    except Exception as e:
        return None, f"Error: {str(e)}"

# Sidebar for search/filter
with st.sidebar:
    st.header("🔍 Search & Filter")
    search_tracking = st.text_input("Tracking Number")
    search_courier = st.text_input("Courier")
    search_status = st.selectbox(
        "Status",
        ["All", "Pending", "In Transit", "Out for Delivery", "Delivered", "Delayed", "Cancelled"]
    )
    
    if st.button("Search", use_container_width=True):
        params = {}
        if search_tracking:
            params["tracking_number"] = search_tracking
        if search_courier:
            params["courier"] = search_courier
        if search_status != "All":
            params["status"] = search_status
        
        data, error = api_request("GET", "/packages/search/", params=params)
        if error:
            st.error(f"❌ {error}")
        elif data and data.get("success"):
            st.session_state["filtered_packages"] = data.get("data", [])
            st.success(f"✅ Found {len(st.session_state['filtered_packages'])} packages")
        else:
            st.info("No packages found")

# Tabs for different views
tab1, tab2, tab3 = st.tabs(["📋 All Packages", "➕ Add Package", "✏️ Update/Delete"])

# ============ TAB 1: Display Packages ============
with tab1:
    st.subheader("All Packages")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        if st.button("🔄 Refresh", use_container_width=False):
            st.session_state.pop("filtered_packages", None)
            st.rerun()
    
    # Fetch packages
    packages_to_display = st.session_state.get("filtered_packages")
    
    if packages_to_display is None:
        data, error = api_request("GET", "/packages/")
        if error:
            st.error(f"❌ {error}")
        elif data and data.get("success"):
            packages_to_display = data.get("data", [])
        else:
            packages_to_display = []
    
    if packages_to_display:
        # Convert to DataFrame
        df = pd.DataFrame(packages_to_display)
        
        # Format the dataframe
        if 'expected_delivery' in df.columns:
            df['expected_delivery'] = pd.to_datetime(df['expected_delivery']).dt.date
        
        # Display metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Packages", len(df))
        with col2:
            in_transit = len(df[df['status'] == 'In Transit']) if 'status' in df.columns else 0
            st.metric("In Transit", in_transit)
        with col3:
            delivered = len(df[df['status'] == 'Delivered']) if 'status' in df.columns else 0
            st.metric("Delivered", delivered)
        with col4:
            pending = len(df[df['status'] == 'Pending']) if 'status' in df.columns else 0
            st.metric("Pending", pending)
        
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "id": "ID",
                "tracking_number": "Tracking #",
                "courier": "Courier",
                "status": st.column_config.TextColumn("Status"),
                "expected_delivery": st.column_config.DateColumn("Expected Delivery"),
                "origin": "Origin",
                "destination": "Destination",
                "notes": "Notes"
            }
        )
    else:
        st.info("No packages found. Add one to get started!")

# ============ TAB 2: Add Package ============
with tab2:
    st.subheader("Add New Package")
    
    with st.form("add_package_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            tracking_number = st.text_input("Tracking Number *", max_chars=50)
            courier = st.text_input("Courier *", max_chars=100)
            status = st.selectbox(
                "Status *",
                ["Pending", "In Transit", "Out for Delivery", "Delivered", "Delayed", "Cancelled"]
            )
            origin = st.text_input("Origin *")
        
        with col2:
            destination = st.text_input("Destination *")
            expected_delivery = st.date_input(
                "Expected Delivery *",
                min_value=date.today()
            )
            notes = st.text_area("Notes", height=100)
        
        submitted = st.form_submit_button("➕ Add Package", use_container_width=True)
        
        if submitted:
            if not tracking_number or not courier or not origin or not destination:
                st.error("❌ Please fill in all required fields (*)")
            else:
                payload = {
                    "tracking_number": tracking_number,
                    "courier": courier,
                    "status": status,
                    "origin": origin,
                    "destination": destination,
                    "expected_delivery": expected_delivery.isoformat(),
                    "notes": notes or None,
                }
                
                data, error = api_request("POST", "/packages/", json=payload)
                
                if error:
                    st.error(f"❌ {error}")
                elif data and data.get("success"):
                    st.success("✅ Package added successfully!")
                    st.json(data.get("data"))
                    st.balloons()

# ============ TAB 3: Update/Delete Package ============
with tab3:
    st.subheader("Update or Delete Package")
    
    # Select package by ID
    package_id = st.number_input("Package ID", min_value=1, step=1)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔍 Load Package", use_container_width=True):
            data, error = api_request("GET", f"/packages/{package_id}")
            if error:
                st.error(f"❌ {error}")
            elif data and data.get("success"):
                st.session_state["current_package"] = data.get("data")
                st.success("✅ Package loaded!")
    
    with col2:
        if st.button("🗑️ Delete Package", use_container_width=True, type="secondary"):
            if st.session_state.get("confirm_delete"):
                data, error = api_request("DELETE", f"/packages/{package_id}")
                if error:
                    st.error(f"❌ {error}")
                elif data and data.get("success"):
                    st.success("✅ Package deleted!")
                    st.session_state.pop("current_package", None)
                    st.session_state.pop("confirm_delete", None)
            else:
                st.session_state["confirm_delete"] = True
                st.warning("⚠️ Click again to confirm deletion")
    
    # Update form
    if "current_package" in st.session_state:
        pkg = st.session_state["current_package"]
        st.divider()
        st.write("**Current Package Details:**")
        st.json(pkg)
        
        with st.form("update_package_form"):
            st.write("**Update Package:**")
            
            col1, col2 = st.columns(2)
            
            with col1:
                new_status = st.selectbox(
                    "Status",
                    ["Pending", "In Transit", "Out for Delivery", "Delivered", "Delayed", "Cancelled"],
                    index=["Pending", "In Transit", "Out for Delivery", "Delivered", "Delayed", "Cancelled"].index(pkg.get("status", "Pending"))
                )
                new_courier = st.text_input("Courier", value=pkg.get("courier", ""))
            
            with col2:
                current_date = datetime.strptime(pkg.get("expected_delivery"), "%Y-%m-%d").date()
                new_delivery = st.date_input("Expected Delivery", value=current_date)
                new_notes = st.text_area("Notes", value=pkg.get("notes", "") or "")
            
            if st.form_submit_button("💾 Update Package", use_container_width=True):
                updates = {}
                if new_status != pkg.get("status"):
                    updates["status"] = new_status
                if new_courier != pkg.get("courier"):
                    updates["courier"] = new_courier
                if new_delivery != current_date:
                    updates["expected_delivery"] = new_delivery.isoformat()
                if new_notes != (pkg.get("notes") or ""):
                    updates["notes"] = new_notes
                
                if updates:
                    data, error = api_request("PUT", f"/packages/{package_id}", json=updates)
                    if error:
                        st.error(f"❌ {error}")
                    elif data and data.get("success"):
                        st.success("✅ Package updated successfully!")
                        st.session_state["current_package"] = data.get("data")
                        st.rerun()
                else:
                    st.info("No changes to update")

# Footer
st.divider()
st.caption("📦 Package Delivery Tracker | Built with FastAPI & Streamlit")