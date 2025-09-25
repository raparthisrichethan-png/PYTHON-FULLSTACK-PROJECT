#frontend ----> API ----> logic ----> database--->Response
#API/main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sys,os
from datetime import date

# Import PackageManager from src
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from SRC.logic import PackageManager

#-----------------------------APP Setup-------------------------------
app = FastAPI(title="Package Delivery Tracker API",version="1.0")

#-------------------------Allow Frontend (Streamlit/React) call the API-------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all origins (frontend can be hosted anywhere)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Creating a PackageManager instance
package_manager = PackageManager()


#-----------------------------Data Models-------------------------------
class PackageCreate(BaseModel):
    """
    Schema for creating a package
    """
    tracking_number: str
    courier: str
    status: str
    expected_delivery: date
    origin: str
    destination:str
    notes: str
class PackageUpdate(BaseModel):
    """
    Schema for updating a package
    """
    expected_delivery: str | None = None

#-----------------------------API Endpoints-------------------------------
@app.get("/")
def home():
    return {"message": "Welcome to the Package Delivery Tracker API"}
@app.get("/packages/")
def get_packages():
    """Fetch all packages"""
    try:
        result = package_manager.get_all_packages()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
@app.post("/packages/")
def create_package(package: PackageCreate):
    """Add a new package"""
    try:
        result = package_manager.add_package(
            package.tracking_number,
            package.courier,
            package.status,
            package.expected_delivery,
            package.origin,
            package.destination,
            package.notes
        )
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
@app.put("/packages/{id}")
def update_package(id: int, package: PackageUpdate):
    """Update an existing package"""
    try:
        updates = {k: v for k, v in package.dict().items() if v is not None}
        result = package_manager.update_package(id, updates)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
@app.delete("/packages/{id}")
def delete_package(id: int):
    """Delete a package"""
    try:
        result = package_manager.delete_package(id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# To run the app: uvicorn API.main:app --reload
if __name__=="__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)