# backend/connectors/telephony_connector.py
from panoramisk import Manager
from fastapi import HTTPException
from sqlalchemy.orm import Session
import models
import asyncio

async def get_asterisk_manager(db: Session, server_id: int):
    server = db.query(models.FreeSwitchServer).filter(models.FreeSwitchServer.id == server_id).first() # Assuming a generic telephony server model
    if not server:
        raise HTTPException(status_code=404, detail="Telephony server not found.")
    
    # password = decrypt_value(server.secret)
    password = server.secret

    manager = Manager(
        loop=asyncio.get_running_loop(), host=server.host, port=server.port or 5038,
        username=server.username, secret=password
    )
    try:
        await manager.connect()
        return manager
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not connect to Asterisk: {e}")

# You would add a similar connector for FreeSWITCH using httpx
