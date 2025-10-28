# backend/routers/traffic.py

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.orm import Session
import database
from security import get_user_from_token_ws
from connectors.mikrotik_connector import create_dedicated_mikrotik_connection
import asyncio
import logging

router = APIRouter()

# --- WebSocket for Live Interface Traffic ---

@router.websocket("/ws/traffic/{device_id}")
async def websocket_traffic_endpoint(
    websocket: WebSocket, 
    device_id: int, 
    token: str,
    db: Session = Depends(database.get_db)
):
    user = await get_user_from_token_ws(token, db)
    if not user:
        await websocket.close(code=1008, reason="Invalid token")
        return
    
    await websocket.accept()

    api_connection = create_dedicated_mikrotik_connection(db, device_id)
    if not api_connection:
        await websocket.close(code=1011, reason="Failed to connect to MikroTik device.")
        return

    try:
        # Get the list of interfaces to monitor
        interface_resource = api_connection.get_resource('/interface')
        interfaces = interface_resource.get()
        interface_names = [iface['name'] for iface in interfaces if not iface.get('disabled') == 'true']
        
        # MikroTik's monitor-traffic can handle multiple interfaces at once
        # However, the python library might not support it directly in a simple loop.
        # A more robust solution involves running the monitor command in a separate thread.
        # For simplicity, we'll monitor all interfaces in a loop.

        # Send the list of interfaces to the frontend first
        await websocket.send_json({"type": "interfaces_list", "data": interface_names})

        last_stats = {}

        while True:
            current_stats = {}
            rates = {}
            
            # Get current stats for all interfaces
            stats_list = interface_resource.get(proplist="name,rx-byte,tx-byte")
            for stats in stats_list:
                current_stats[stats['name']] = {'rx': int(stats['rx-byte']), 'tx': int(stats['tx-byte'])}

            if last_stats:
                for name in interface_names:
                    if name in current_stats and name in last_stats:
                        rx_rate = (current_stats[name]['rx'] - last_stats[name]['rx']) # bytes per second
                        tx_rate = (current_stats[name]['tx'] - last_stats[name]['tx']) # bytes per second
                        rates[name] = {'rx_bps': rx_rate * 8, 'tx_bps': tx_rate * 8} # bits per second
            
            last_stats = current_stats
            
            if rates:
                await websocket.send_json({"type": "traffic_update", "data": rates})

            await asyncio.sleep(1) # Send updates every second

    except WebSocketDisconnect:
        logging.info(f"Traffic WebSocket for device {device_id} disconnected.")
    except Exception as e:
        logging.error(f"Traffic WebSocket error for device {device_id}: {e}")
    finally:
        if api_connection:
            api_connection.close()
