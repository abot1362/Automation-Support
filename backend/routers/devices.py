from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models, schemas, database
from security import get_current_user # Dependency for checking login

router = APIRouter(
    prefix="/api/devices",
    tags=["Devices"],
    dependencies=[Depends(get_current_user)] # Protect all endpoints in this router
)

@router.post("/", response_model=schemas.Device, status_code=201)
def create_device(device: schemas.DeviceCreate, db: Session = Depends(database.get_db)):
    """Creates a new device entry in the database."""
    # In a real app, encrypt the password before saving
    # device.password = encrypt_value(device.password)
    db_device = models.Device(**device.dict())
    db.add(db_device)
    db.commit()
    db.refresh(db_device)
    return db_device

@router.get("/", response_model=List[schemas.Device])
def read_devices(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    """Retrieves a list of all configured devices."""
    devices = db.query(models.Device).offset(skip).limit(limit).all()
    return devices

@router.get("/{device_id}", response_model=schemas.Device)
def read_device(device_id: int, db: Session = Depends(database.get_db)):
    """Retrieves a single device by its ID."""
    db_device = db.query(models.Device).filter(models.Device.id == device_id).first()
    if db_device is None:
        raise HTTPException(status_code=404, detail="Device not found")
    return db_device

@router.delete("/{device_id}", status_code=204)
def delete_device(device_id: int, db: Session = Depends(database.get_db)):
    """Deletes a device from the database."""
    db_device = db.query(models.Device).filter(models.Device.id == device_id).first()
    if db_device is None:
        raise HTTPException(status_code=404, detail="Device not found")
    db.delete(db_device)
    db.commit()
    return
