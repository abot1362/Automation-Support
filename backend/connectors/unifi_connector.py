# connectors/unifi_connector.py

from pyunifi.controller import Controller
from fastapi import HTTPException
from sqlalchemy.orm import Session
import models

def get_unifi_controller(db: Session, controller_id: int):
    """Initializes and returns a client for a specific UniFi Controller."""
    controller_db = db.query(models.UniFiController).filter(models.UniFiController.id == controller_id).first()
    if not controller_db:
        raise HTTPException(status_code=404, detail="UniFi Controller not found.")

    try:
        # password = decrypt_value(controller_db.password)
        password = controller_db.password # Placeholder
        
        client = Controller(
            host=controller_db.host,
            username=controller_db.username,
            password=password,
            port=controller_db.port or 8443,
            site_id=controller_db.site_id or 'default',
            ssl_verify=False # For production, manage certs properly
        )
        # The library logs in automatically on the first API call.
        return client
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to initialize UniFi Controller client: {e}")
