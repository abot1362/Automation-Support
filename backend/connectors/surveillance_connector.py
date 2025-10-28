# connectors/surveillance_connector.py
from fastapi import HTTPException
from sqlalchemy.orm import Session
import models
# You need to implement the actual logic for each class
# This is the structural template

class BaseSurveillanceConnector:
    def __init__(self, system_model: models.SurveillanceSystem):
        self.system = system_model
        # self.password = decrypt_value(system_model.password)
        self.password = system_model.password # Placeholder

    async def get_cameras(self): raise NotImplementedError
    async def get_live_stream_url(self, camera_id): raise NotImplementedError
    # ... other interface methods

class ShinobiConnector(BaseSurveillanceConnector):
    # ... Implementation for Shinobi ...
    pass

class ZoneMinderConnector(BaseSurveillanceConnector):
    # ... Implementation for ZoneMinder ...
    pass

class HikvisionConnector(BaseSurveillanceConnector):
    # ... Implementation for Hikvision ...
    pass

def get_surveillance_connector(db: Session, system_id: int):
    system = db.query(models.SurveillanceSystem).filter(models.SurveillanceSystem.id == system_id).first()
    if not system:
        raise HTTPException(status_code=404, detail="Surveillance system not found.")
    
    if system.system_type == 'Shinobi':
        return ShinobiConnector(system)
    elif system.system_type == 'ZoneMinder':
        return ZoneMinderConnector(system)
    elif system.system_type == 'Hikvision':
        return HikvisionConnector(system)
    else:
        raise HTTPException(status_code=501, detail=f"Connector for '{system.system_type}' is not implemented.")
