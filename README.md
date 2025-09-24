# package delivery tracker

The Package Delivery Tracker is a software application designed to help users efficiently track and manage the status of packages during shipment. It allows users to log package details such as tracking number, courier service, origin, destination, and expected delivery dates.
This project is ideal for individuals or small businesses to maintain an organized record of all outgoing and incoming parcels, helping to avoid lost or delayed shipments. Built with Python and SQL, it emphasizes database management, CRUD operations, and user-friendly data handling.

## Features

**User Authentication**
    Allow users to create accounts and log in.
    Each user can track their own packages securely.
**Package History / Tracking Timeline**
    Keep a log of all status changes and timestamps for each package.
    Users can see the full journey of their package.
**Search and Filter**
    Search packages by tracking number, courier, status, or destination.
    Filter packages by status (e.g., Delivered, In Transit).
**Live Status Updates**
    Track package progress with near real-time status changes.



##  Project Structure

PACKAGE DELIVERY TRACKER/
|
|
|---SRC/   #core application logic
|    |---logic.py    # Business logic and package operations
operations
|    |__db.py    # Database connection and queries
|
|----API/
|    |__main.py    # API server entry point
|
|----FRONTEND/
|    |__app.py    # Frontend application (CLI, GUI, or web)
|
|_____requirements.txt   # Python dependencies
|
|
|_____Readme.md 
|
|
|_____.env  # Environment variables (e.g., DB credentials)


## Quick Start

### Prerequisites

- Python 3.8 or higher
- A Supabase account
- Git(Push,Cloning)

### 1. Clone or Download the Project
# Option 1: Clone with Git
git clone <repository-url>

# Option 2: Download and extract zip files

### 2. Install Dependicies
pip install -r requirements.txt

### 3. Set up Supabase Database
1. Create a Supabse Project:

2. Create a Task  table:

- Go to the SQL Editor in your Supabase
dashboard
- Run this SQL command:
```sql
    CREATE TABLE packages (
    id serial PRIMARY KEY,
    tracking_number TEXT UNIQUE NOT NULL,
    courier TEXT NOT NULL,
    status TEXT DEFAULT 'Pending',
    expected_delivery TEXT,
    origin TEXT,
    destination TEXT,
    notes TEXT
);
```
  3.Get Your Credentials

### 4.Configure Environment Variables

1.create a '.env' file in the project

2.Add your supabse credentials to '.env':

**Examples:**
SUPABASE_URL="https://jeeghcxmzjprytcfnjig.supabase.co"
SUPABASE_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ.9eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImplZWdoY3htempwcnl0Y2ZuamlnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTgwODIyODgsImV4cCI6MjA3MzY1ODI4OH0.BOki2IRAL0cChLO-zBqenMWhIsTwnopmdEeeNYsK9-g"

### 5. Run the Application
## Streamlit Frontend
streamlit run frontend/app.py
The app will open in your browser at 'https://localhost:8000'

## Fast api
cd API
The api will will be available at 'https://localhost:8050'

## How to use
    Open the app (web, desktop, or CLI).

    Add a package by entering tracking number, courier, origin, destination, and expected delivery date.

    View all packages with their current status and details.

    Update package status as the delivery progresses.

    Search or filter packages by tracking number or status.

    Delete or edit package info if needed.
## Technical Details

## Technologies Used

-**Front end**: Streamlit (Python web Framework)

-**back end**:FastApI (Python Rest API Framework)

-**database**:Supabase (PostgreSQL-basedbackend-as-a-service)

-**Language**: Python 3.8+

## Key Components

1. **'src/db.py'**:Database operations
    -Handles all CRUD operations with Supabase
2. **'src/logic.py**:Business logic 
    -Task validation and processing

## Troubleshooting

# Common Issues

1.**"Module not found" errors**
    -Make sure you've installed all dependencies:pip install -r requirements.txt
    - Check that you're running commands from the correct directory

## Future Enhancements
1.**Integration with Courier APIs**:
    Automatically fetch real-time tracking updates directly from courier services (FedEx, UPS, DHL, USPS).

2.**Real-Time Push Notifications**:
    Implement real-time alerts via email, SMS, or mobile push notifications when package status changes or issues arise.

3. **Mobile App Development**:
    Create native Android/iOS apps for better accessibility on the go.

4. **Advanced Analytics & Reporting**:

Provide users and businesses with delivery performance analytics.

Generate reports on average delivery times, delays, and courier efficiency.

5. **AI-Powered Delay Predictions**:

Use machine learning models to predict potential delays based on historical data and current trends.

## Support

If you encounter any issues or have questions:
    --phno.:9119994143
    --email:raparthisrichethan@gmail.com