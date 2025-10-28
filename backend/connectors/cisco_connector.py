# connectors/cisco_connector.py

from netmiko import ConnectHandler
from ncclient import manager
from fastapi import HTTPException
from sqlalchemy.orm import Session
import models

def get_cisco_handler(db: Session, device_id: int):
    """
    Returns a live connection handler (Netmiko or ncclient) for a Cisco device.
    The caller is responsible for disconnecting.
    """
    device = db.query(models.Device).filter(models.Device.id == device_id).first()
    if not device or device.vendor != 'Cisco' or not device.is_active:
        raise HTTPException(status_code=404, detail="Active Cisco device not found.")

    # password = decrypt_value(device.password)
    password = device.password # Placeholder

    connection_params = {
        'host': device.host,
        'username': device.username,
        'password': password,
    }

    if device.management_protocol == 'ssh':
        connection_params['device_type'] = device.os_type or 'cisco_ios'
        connection_params['port'] = device.port or 22
        try:
            return ConnectHandler(**connection_params)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"SSH connection to {device.name} failed: {e}")
            
    elif device.management_protocol == 'netconf':
        connection_params['port'] = device.port or 830
        connection_params['hostkey_verify'] = False # For production, this should be True
        connection_params['device_params'] = {'name': 'iosxe'} # Adjust based on OS
        try:
            return manager.connect(**connection_params)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"NETCONF connection to {device.name} failed: {e}")
            
    else:
        raise HTTPException(status_code=400, detail=f"Unsupported management protocol for Cisco device: {device.management_protocol}")

def close_cisco_handler(handler, protocol: str):
    if handler:
        try:
            if protocol == 'ssh':
                handler.disconnect()
            elif protocol == 'netconf':
                handler.close_session()
        except Exception:
            pass # Ignore errors on close
