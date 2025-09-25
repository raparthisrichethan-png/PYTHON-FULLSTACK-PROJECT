# main.py
import subprocess
import sys
import os

if __name__ == "__main__":
    print("🚀 Starting Package Delivery Tracker...")

    # Get current directory (where main.py is located)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    app_path = os.path.join(current_dir, "app.py")

    # Run Streamlit
    subprocess.run([sys.executable, "-m", "streamlit", "run", app_path])
