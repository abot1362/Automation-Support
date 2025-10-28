# connectors/mikrotik_connector.py

import routeros_api
from fastapi import HTTPException
from sqlalchemy.orm import Session
import models
import logging

# A dictionary to manage connection pools for multiple devices
connection_pools = {}

def get_api_connector(db: Session, device_id: int):
    """
    Gets a connection from a pool for a specific MikroTik device.
    Creates a new pool if one doesn't exist.
    """
    device = db.query(models.Device).filter(models.Device.id == device_id).first()
    if not device or device.vendor != 'MikroTik' or not device.is_active:
        raise HTTPException(status_code=404, detail="Active MikroTik device not found.")

    if device_id in connection_pools:
        pool = connection_pools[device_id]
        if not pool.is_closed():
            try:
                return pool.get_api()
            except routeros_api.exceptions.RouterOsApiConnectionError:
                logging.warning(f"Connection pool for device {device_id} seems stale. Reconnecting.")
                pool.disconnect()
    
    try:
        # Decrypt password before connecting
        # password = decrypt_value(device.password)
        password = device.password # Placeholder for decrypted password
        
        pool = routeros_api.RouterOsApiPool(
            host=device.host,
            username=device.username,
            password=password,
            port=device.port or 8728,
            plaintext_login=True
        )
        connection_pools[device_id] = pool
        return pool.get_api()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not connect to MikroTik device {device.name}: {e}")

def create_dedicated_mikrotik_connection(db: Session, device_id: int):
    """Creates a single, dedicated connection for tasks like CLI or monitoring."""
    device = db.query(models.Device).filter(models.Device.id == device_id).first()
    if not device or device.vendor != 'MikroTik':
        return None
    
    try:
        # password = decrypt_value(device.password)
        password = device.password # Placeholder
        
        connection = routeros_api.connect(
            host=device.host,
            username=device.username,
            password=password,
            port=device.port or 8728,
            plaintext_login=True
        )
        return connection
    except Exception as e:
        logging.error(f"Failed to create dedicated MikroTik connection to {device.name}: {e}")
        return None
