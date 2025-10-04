from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from datetime import date
import sys, os
import logging

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from SRC.logic import PackageManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ----------------------------- App Setup -------------------------------
app = FastAPI(
    title="Package Delivery Tracker API",
    version="2.0",
    description="API for tracking package deliveries"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

package_manager = PackageManager()

# ----------------------------- Data Models -------------------------------
class PackageCreate(BaseModel):
    tracking_number: str = Field(..., min_length=1, max_length=50)
    courier: str = Field(..., min_length=1, max_length=100)
    status: str
    expected_delivery: date
    origin: str
    destination: str
    notes: str | None = None

    class Config:
        json_schema_extra = {
            "example": {
                "tracking_number": "1Z999AA10123456784",
                "courier": "UPS",
                "status": "In Transit",
                "expected_delivery": "2025-10-15",
                "origin": "New York, NY",
                "destination": "Los Angeles, CA",
                "notes": "Fragile item"
            }
        }

class PackageUpdate(BaseModel):
    tracking_number: str | None = Field(None, min_length=1, max_length=50)
    courier: str | None = Field(None, min_length=1, max_length=100)
    status: str | None = None
    expected_delivery: date | None = None
    origin: str | None = None
    destination: str | None = None
    notes: str | None = None

class PackageResponse(BaseModel):
    success: bool
    data: dict | list | None = None
    error: str | None = None

# ----------------------------- API Endpoints -------------------------------
@app.get("/", tags=["Health"])
def home():
    """Health check endpoint."""
    return {
        "message": "Welcome to the Package Delivery Tracker API",
        "version": "2.0",
        "status": "operational"
    }

@app.get("/packages/", tags=["Packages"], response_model=PackageResponse)
def get_packages(
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0)
):
    """
    Retrieve all packages with pagination.
    
    - **limit**: Maximum number of packages to return (1-500)
    - **offset**: Number of packages to skip
    """
    logger.info(f"Fetching packages with limit={limit}, offset={offset}")
    result = package_manager.get_all_packages(limit=limit, offset=offset)
    
    if not result.get("success"):
        raise HTTPException(status_code=500, detail=result.get("error", "Unknown error"))
    
    return result

@app.get("/packages/search/", tags=["Packages"], response_model=PackageResponse)
def search_packages(
    tracking_number: str | None = None,
    courier: str | None = None,
    status: str | None = None
):
    """
    Search packages by various criteria.
    
    - **tracking_number**: Partial or full tracking number
    - **courier**: Courier name
    - **status**: Package status
    """
    logger.info(f"Searching packages: tracking={tracking_number}, courier={courier}, status={status}")
    result = package_manager.search_packages(
        tracking_number=tracking_number,
        courier=courier,
        status=status
    )
    
    if not result.get("success"):
        raise HTTPException(status_code=500, detail=result.get("error", "Unknown error"))
    
    return result

@app.get("/packages/{id}", tags=["Packages"], response_model=PackageResponse)
def get_package(id: int):
    """Retrieve a single package by ID."""
    logger.info(f"Fetching package {id}")
    result = package_manager.get_package(id)
    
    if not result.get("success"):
        raise HTTPException(
            status_code=404,
            detail=result.get("error", "Package not found")
        )
    
    return result

@app.post("/packages/", tags=["Packages"], response_model=PackageResponse)
def create_package(pkg: PackageCreate):
    """Create a new package."""
    logger.info(f"Creating package with tracking number: {pkg.tracking_number}")
    result = package_manager.add_package(
        pkg.tracking_number,
        pkg.courier,
        pkg.status,
        pkg.expected_delivery,
        pkg.origin,
        pkg.destination,
        pkg.notes
    )
    
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("error", "Unknown error"))
    
    return result

@app.put("/packages/{id}", tags=["Packages"], response_model=PackageResponse)
def update_package(id: int, pkg: PackageUpdate):
    """Update an existing package."""
    logger.info(f"Updating package {id}")
    updates = pkg.model_dump(exclude_none=True)
    
    if not updates:
        raise HTTPException(status_code=400, detail="No fields to update")
    
    result = package_manager.update_package(id, updates)
    
    if not result.get("success"):
        raise HTTPException(
            status_code=404,
            detail=result.get("error", "Package not found")
        )
    
    return result

@app.delete("/packages/{id}", tags=["Packages"], response_model=PackageResponse)
def delete_package(id: int):
    """Delete a package."""
    logger.info(f"Deleting package {id}")
    result = package_manager.delete_package(id)
    
    if not result.get("success"):
        raise HTTPException(
            status_code=404,
            detail=result.get("error", "Package not found")
        )
    
    return result

# ----------------------------- Error Handlers -------------------------------
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Unhandled exception: {str(exc)}")
    return {
        "success": False,
        "error": "An internal server error occurred"
    }

# ----------------------------- Run -------------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)