# connectors/vmware_connector.py

import aiohttp
from fastapi import HTTPException
from sqlalchemy.orm import Session
import models
import logging

# A simple in-memory cache for session tokens to avoid logging in for every request
session_tokens = {}

async def get_vcenter_session_token(db: Session, vcenter_id: int) -> str:
    """
    Authenticates with a vCenter server and returns a session token.
    Uses a simple cache to reuse tokens.
    """
    # In a real-world scenario, you should check token expiration
    if vcenter_id in session_tokens:
        return session_tokens[vcenter_id]

    vcenter = db.query(models.VMwareVCenter).filter(models.VMwareVCenter.id == vcenter_id).first()
    if not vcenter:
        raise HTTPException(status_code=404, detail="vCenter server not found.")

    auth_url = f"https://{vcenter.host}/rest/com/vmware/cis/session"
    # password = decrypt_value(vcenter.password)
    password = vcenter.password # Placeholder
    
    auth = aiohttp.BasicAuth(login=vcenter.username, password=password)
    
    # In production, SSL verification should be enabled and managed properly.
    connector = aiohttp.TCPConnector(ssl=False)
    async with aiohttp.ClientSession(connector=connector) as session:
        try:
            async with session.post(auth_url, auth=auth) as response:
                response.raise_for_status()
                token = (await response.json())['value']
                session_tokens[vcenter_id] = token
                logging.info(f"Successfully obtained session token for vCenter '{vcenter.name}'.")
                return token
        except Exception as e:
            logging.error(f"vCenter authentication failed for '{vcenter.name}': {e}")
            raise HTTPException(status_code=500, detail=f"vCenter authentication failed: {e}")

class VMwareAPIClient:
    """A client for making authenticated requests to the vCenter REST API."""
    def __init__(self, db: Session, vcenter_id: int):
        self.db = db
        self.vcenter_id = vcenter_id
        vcenter = db.query(models.VMwareVCenter).filter(models.VMwareVCenter.id == vcenter_id).first()
        if not vcenter:
            raise HTTPException(status_code=404, detail="vCenter server not found.")
        self.base_url = f"https://{vcenter.host}/rest"
        self.connector = aiohttp.TCPConnector(ssl=False)

    async def get(self, endpoint: str):
        """Sends an authenticated GET request to the vCenter API."""
        token = await get_vcenter_session_token(self.db, self.vcenter_id)
        url = f"{self.base_url}/{endpoint}"
        headers = {"vmware-api-session-id": token}
        
        async with aiohttp.ClientSession(connector=self.connector) as session:
            try:
                async with session.get(url, headers=headers) as response:
                    response.raise_for_status()
                    return await response.json()
            except Exception as e:
                logging.error(f"vCenter API GET request to '{endpoint}' failed: {e}")
                raise HTTPException(status_code=500, detail=f"vCenter API call failed: {e}")
    
    async def post(self, endpoint: str, data: dict = None):
        """Sends an authenticated POST request to the vCenter API."""
        token = await get_vcenter_session_token(self.db, self.vcenter_id)
        url = f"{self.base_url}/{endpoint}"
        headers = {"vmware-api-session-id": token}
        
        async with aiohttp.ClientSession(connector=self.connector) as session:
            try:
                async with session.post(url, headers=headers, json=data) as response:
                    response.raise_for_status()
                    if response.content_length and response.content_length > 0:
                        return await response.json()
                    return {"status": "success"} # For actions that return no content
            except Exception as e:
                logging.error(f"vCenter API POST request to '{endpoint}' failed: {e}")
                raise HTTPException(status_code=500, detail=f"vCenter API call failed: {e}")
