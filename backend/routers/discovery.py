# backend/routers/discovery.py

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, List
import json
import models, schemas, database
from security import get_current_user_from_token
from dependencies import require_permission

router = APIRouter(
    prefix="/api/discovery",
    tags=["Network Discovery"],
    dependencies=[Depends(require_permission("discovery:run"))] # A new permission
)

# --- Connection Manager for broadcasting results to all connected admins ---
class DiscoveryConnectionManager:
    def __init__(self):
        # Connections from admin frontends
        self.frontend_connections: List[WebSocket] = []
        # Connection from the single discovery agent
        self.agent_connection: WebSocket | None = None

    async def connect_frontend(self, websocket: WebSocket):
        await websocket.accept()
        self.frontend_connections.append(websocket)

    def disconnect_frontend(self, websocket: WebSocket):
        self.frontend_connections.remove(websocket)
    
    async def connect_agent(self, websocket: WebSocket):
        await websocket.accept()
        if self.agent_connection:
            # Only allow one agent at a time for simplicity
            await websocket.close(code=1008, reason="Another agent is already connected.")
            return False
        self.agent_connection = websocket
        return True

    def disconnect_agent(self):
        self.agent_connection = None
    
    async def send_command_to_agent(self, command: dict):
        if self.agent_connection:
            await self.agent_connection.send_json(command)
        else:
            raise HTTPException(status_code=503, detail="No discovery agent is connected.")

    async def broadcast_to_frontends(self, message: str):
        for connection in self.frontend_connections:
            await connection.send_text(message)

manager = DiscoveryConnectionManager()
AGENT_SECRET_KEY = "a_very_secret_key_to_authenticate_agents" # Should be in .env

# --- WebSocket for the Discovery Agent ---
@router.websocket("/ws/agent")
async def register_agent(websocket: WebSocket):
    try:
        auth_message = await websocket.receive_json()
        if not (auth_message.get("type") == "agent_auth" and auth_message.get("key") == AGENT_SECRET_KEY):
            await websocket.close(reason="Authentication failed")
            return

        if not await manager.connect_agent(websocket):
            return
            
        await websocket.send_json({"status": "authenticated"})
        print("Discovery agent connected.")

        while True:
            # Listen for results from the agent
            result = await websocket.receive_json()
            # Broadcast results to all connected admin frontends
            await manager.broadcast_to_frontends(json.dumps(result))

    except WebSocketDisconnect:
        manager.disconnect_agent()
        print("Discovery agent disconnected.")

# --- WebSocket for Admin Frontends to receive live results ---
@router.websocket("/ws/subscribe")
async def subscribe_t
