# connectors/proxmox_connector.py

import httpx
from fastapi import HTTPException
from sqlalchemy.orm import Session
import models
import logging

class ProxmoxAPIClient:
    """A client for making authenticated requests to the Proxmox VE API."""
    def __init__(self, db: Session, server_id: int):
        server = db.query(models.ProxmoxServer).filter(models.ProxmoxServer.id == server_id).first()
        if not server:
            raise HTTPException(status_code=404, detail="Proxmox server not found.")
        
        self.base_url = f"https://{server.host}:{server.port or 8006}/api2/json"
        
        # Proxmox API token needs to be in the Authorization header.
        # token_secret = decrypt_value(server.api_token_secret)
        token_secret = server.api_token_secret # Placeholder
        
        self.headers = {
            "Authorization": f"PVEAPIToken={server.api_token_id}={token_secret}"
        }
        self.client = httpx.AsyncClient(verify=False) # In production, manage certs

    async def get(self, endpoint: str):
        """Sends an authenticated GET request to the Proxmox API."""
        url = f"{self.base_url}{endpoint}" # Proxmox endpoints start with a '/'
        try:
            response = await self.client.get(url, headers=self.headers)
            response.raise_for_status()
            # The actual data is usually inside a 'data' key
            return response.json().get('data')
        except httpx.HTTPStatusError as e:
            logging.error(f"Proxmox API Error for GET {endpoint}: {e.response.text}")
            raise HTTPException(status_code=e.response.status_code, detail=f"Proxmox API Error: {e.response.text}")
        except httpx.RequestError as e:
            logging.error(f"Could not connect to Proxmox for GET {endpoint}: {e}")
            raise HTTPException(status_code=503, detail=f"Could not connect to Proxmox server: {e}")

    async def post(self, endpoint: str, data: dict = None):
        """Sends an authenticated POST request (for actions like start/stop)."""
        url = f"{self.base_url}{endpoint}"
        try:
            response = await self.client.post(url, headers=self.headers, json=data)
            response.raise_for_status()
            return response.json().get('data')
        except httpx.HTTPStatusError as e:
            logging.error(f"Proxmox API Error for POST {endpoint}: {e.response.text}")
            raise HTTPException(status_code=e.response.status_code, detail=f"Proxmox API Error: {e.response.text}")
        except httpx.RequestError as e:
            logging.error(f"Could not connect to Proxmox for POST {endpoint}: {e}")
            raise HTTPException(status_code=503, detail=f"Could not connect to Proxmox server: {e}")

    async def close(self):
        await self.client.aclose()
