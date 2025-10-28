from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime
import database
from security import get_current_user
from connectors.surveillance_connector import get_surveillance_connector

router = APIRouter(
    prefix="/api/surveillance/systems",
    tags=["Surveillance"],
    dependencies=[Depends(get_current_user)]
)

# You would have CRUD endpoints for managing the systems themselves here
# POST / , GET / , etc.

@router.get("/{system_id}/info")
async def get_surveillance_system_info(system_id: int, db: Session = Depends(database.get_db)):
    """Gets hardware and system info for a specific surveillance system."""
    connector = get_surveillance_connector(db, system_id)
    return await connector.get_system_info()

@router.get("/{system_id}/cameras")
async def list_cameras(system_id: int, db: Session = Depends(database.get_db)):
    """Lists all cameras for a specific surveillance system."""
    connector = get_surveillance_connector(db, system_id)
    return await connector.get_cameras()

@router.get("/{system_id}/cameras/{camera_id}/live")
async def get_live_stream(system_id: int, camera_id: str, db: Session = Depends(database.get_db)):
    """Gets live stream information for a specific camera."""
    connector = get_surveillance_connector(db, system_id)
    return await connector.get_live_stream_url(camera_id)

# ... other endpoints for playback, download, etc.
