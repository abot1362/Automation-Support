from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import database, schemas
from security import get_current_user
from connectors.mikrotik_connector import get_api_connector

router = APIRouter(
    prefix="/api/mikrotik/devices/{device_id}",
    tags=["MikroTik"],
    dependencies=[Depends(get_current_user)]
)

@router.get("/resources")
def get_mikrotik_resources(device_id: int, db: Session = Depends(database.get_db)):
    """Gets system resources for a specific MikroTik device."""
    api = get_api_connector(db, device_id)
    resources = api.get_resource('/system/resource').get()
    return resources[0] if resources else {}

@router.get("/hotspot/users")
def get_hotspot_users(device_id: int, db: Session = Depends(database.get_db)):
    """Gets the list of configured Hotspot users."""
    api = get_api_connector(db, device_id)
    return api.get_resource('/ip/hotspot/user').get()

@router.get("/ppp/secrets")
def get_ppp_secrets(device_id: int, db: Session = Depends(database.get_db)):
    """Gets the list of PPP secrets (for VPN/PPPoE)."""
    api = get_api_connector(db, device_id)
    return api.get_resource('/ppp/secret').get()

# ... other MikroTik specific endpoints (active users, profiles, etc.)
