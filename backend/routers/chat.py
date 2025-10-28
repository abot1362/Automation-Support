# backend/routers/chat.py

from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect, Query, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
import json

import models, schemas, database
from security import get_current_user_from_token, get_user_from_token_ws
from dependencies import require_permission
import shutil # For saving uploaded files

router = APIRouter(
    prefix="/api/chat",
    tags=["Chat"]
)

# --- WebSocket Connection Manager ---
class ChatConnectionManager:
    def __init__(self):
        self.active_connections: dict[int, List[WebSocket]] = {}

    async def connect(self, room_id: int, websocket: WebSocket):
        await websocket.accept()
        if room_id not in self.active_connections:
            self.active_connections[room_id] = []
        self.active_connections[room_id].append(websocket)

    def disconnect(self, room_id: int, websocket: WebSocket):
        if room_id in self.active_connections:
            self.active_connections[room_id].remove(websocket)

    async def broadcast_to_room(self, room_id: int, message: dict):
        if room_id in self.active_connections:
            for connection in self.active_connections[room_id]:
                await connection.send_json(message)

manager = ChatConnectionManager()

# --- WebSocket Endpoint for Real-time Messaging ---

@router.websocket("/ws/{room_id}")
async def websocket_chat_endpoint(
    websocket: WebSocket, 
    room_id: int, 
    token: str = Query(...),
    db: Session = Depends(database.get_db)
):
    user = await get_user_from_token_ws(token, db)
    if not user:
        await websocket.close(code=1008, reason="Invalid token")
        return

    # Security check: ensure user is a participant of the room
    participant = db.query(models.ChatParticipant).filter(
        models.ChatParticipant.room_id == room_id,
        models.ChatParticipant.user_id == user.id
    ).first()
    if not participant:
        await websocket.close(code=1008, reason="Not a member of this room")
        return
        
    await manager.connect(room_id, websocket)
    try:
        while True:
            data = await websocket.receive_json()
            
            # Save message to database
            new_message = models.ChatMessage(
                room_id=room_id,
                user_id=user.id,
                message_type=data.get('type', 'text'),
                text_content=data.get('content')
                # ... handle other message types like file, location ...
            )
            db.add(new_message)
            db.commit()
            db.refresh(new_message)
            
            # Broadcast message to all clients in the room
            message_to_broadcast = {
                "id": new_message.id,
                "user": user.username,
                "type": new_message.message_type,
                "content": new_message.text_content,
                "timestamp": new_message.timestamp.isoformat()
            }
            await manager.broadcast_to_room(room_id, message_to_broadcast)

    except WebSocketDisconnect:
        manager.disconnect(room_id, websocket)


# --- REST API Endpoints for Chat Management ---

@router.get("/my-rooms", dependencies=[Depends(get_current_user_from_token)])
def get_my_chat_rooms(current_user: models.User = Depends(get_current_user_from_token), db: Session = Depends(database.get_db)):
    """Gets the list of chat rooms the current user is a member of."""
    participations = db.query(models.ChatParticipant).filter(models.ChatParticipant.user_id == current_user.id).all()
    rooms = [p.room for p in participations]
    return rooms

@router.get("/rooms/{room_id}/messages", dependencies=[Depends(get_current_user_from_token)])
def get_chat_history(room_id: int, current_user: models.User = Depends(get_current_user_from_token), db: Session = Depends(database.get_db)):
    """Gets the message history for a specific room."""
    # ... (Security check to ensure user is a participant) ...
    messages = db.query(models.ChatMessage).filter(models.ChatMessage.room_id == room_id).order_by(models.ChatMessage.timestamp.asc()).all()
    return messages

@router.post("/upload", dependencies=[Depends(get_current_user_from_token)])
async def upload_chat_file(file: UploadFile = File(...)):
    """Handles file uploads for chat attachments."""
    # Define a safe path to store files
    file_path = f"uploads/chat/{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Return the URL that can be used to access the file
    # This URL will be sent in a WebSocket message of type 'file' or 'image'
    return {"file_url": f"/files/chat/{file.filename}", "file_name": file.filename, "file_size_kb": round(file.size / 1024)}

# --- Admin Endpoints for Room Management ---

@router.post("/rooms", dependencies=[Depends(require_permission("chat:manage:rooms"))])
def create_chat_room(room_data: schemas.ChatRoomCreate, db: Session = Depends(database.get_db)):
    """(Admin) Creates a new chat room."""
    db_room = models.ChatRoom(name=room_data.name, description=room_data.description)
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return db_room

# ... (Other admin endpoints for adding/removing participants, deleting rooms, etc.) ...
