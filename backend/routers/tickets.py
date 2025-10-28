# backend/routers/tickets.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import models, schemas, database
from security import get_current_user_from_token
from dependencies import require_permission # Dependency برای کنترل دسترسی

router = APIRouter(
    prefix="/api/tickets",
    tags=["Support Tickets"]
)

# --- API Endpoints for Admins/Support Staff ---

@router.get(
    "/all", 
    response_model=List[schemas.Ticket], 
    dependencies=[Depends(require_permission("tickets:read:all"))]
)
def read_all_tickets(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    """
    (Admin) Gets a list of all tickets in the system.
    """
    tickets = db.query(models.Ticket).order_by(models.Ticket.updated_at.desc()).offset(skip).limit(limit).all()
    return tickets

@router.put(
    "/{ticket_id}/assign", 
    response_model=schemas.Ticket,
    dependencies=[Depends(require_permission("tickets:assign"))]
)
def assign_ticket(ticket_id: int, assignment_data: schemas.TicketAssignment, db: Session = Depends(database.get_db)):
    """
    (Admin/Manager) Assigns a ticket to a specific user.
    """
    db_ticket = db.query(models.Ticket).filter(models.Ticket.id == ticket_id).first()
    if not db_ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
        
    assignee = db.query(models.User).filter(models.User.id == assignment_data.assignee_id).first()
    if not assignee:
        raise HTTPException(status_code=404, detail="Assignee user not found")

    db_ticket.assigned_to_user_id = assignment_data.assignee_id
    db.commit()
    db.refresh(db_ticket)
    return db_ticket

@router.put(
    "/{ticket_id}/status",
    response_model=schemas.Ticket,
    dependencies=[Depends(require_permission("tickets:update:status"))]
)
def update_ticket_status(ticket_id: int, status_update: schemas.TicketStatusUpdate, db: Session = Depends(database.get_db)):
    """
    (Admin/Support) Updates the status of a ticket (e.g., 'in_progress', 'closed').
    """
    db_ticket = db.query(models.Ticket).filter(models.Ticket.id == ticket_id).first()
    if not db_ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
        
    db_ticket.status = status_update.status
    db.commit()
    db.refresh(db_ticket)
    return db_ticket

# --- API Endpoints for All Logged-in Users (including End-Users) ---

@router.post(
    "/", 
    response_model=schemas.Ticket, 
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_permission("tickets:create"))]
)
def create_ticket(
    ticket: schemas.TicketCreate, 
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user_from_token)
):
    """
    Creates a new support ticket. Automatically assigned to the user's manager if available.
    """
    # Create the ticket object
    db_ticket = models.Ticket(
        title=ticket.title,
        created_by_user_id=current_user.id
    )
    # If the user has a manager, auto-assign the ticket
    if current_user.manager_id:
        db_ticket.assigned_to_user_id = current_user.manager_id
    
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    
    # Also create the first reply with the initial message
    first_reply = models.TicketReply(
        message=ticket.initial_message,
        ticket_id=db_ticket.id,
        user_id=current_user.id
    )
    db.add(first_reply)
    db.commit()
    
    return db_ticket

@router.get(
    "/my", 
    response_model=List[schemas.Ticket],
    dependencies=[Depends(require_permission("tickets:read:own"))]
)
def read_my_tickets(
    db: Session = Depends(database.get_db), 
    current_user: models.User = Depends(get_current_user_from_token)
):
    """
    Gets a list of all tickets created by the current user.
    """
    return db.query(models.Ticket).filter(models.Ticket.created_by_user_id == current_user.id).order_by(models.Ticket.updated_at.desc()).all()

@router.get(
    "/{ticket_id}", 
    response_model=schemas.TicketWithReplies
)
def read_ticket_details(
    ticket_id: int,
    db: Session = Depends(database.get_db), 
    current_user: models.User = Depends(get_current_user_from_token)
):
    """
    Gets the full details and all replies for a single ticket.
    Ensures the user has permission to view it.
    """
    db_ticket = db.query(models.Ticket).filter(models.Ticket.id == ticket_id).first()
    if not db_ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    # Security check: User must be the creator, assignee, or an admin with full read access.
    user_permissions = {p.name for p in current_user.role.permissions}
    if not (db_ticket.created_by_user_id == current_user.id or 
            db_ticket.assigned_to_user_id == current_user.id or
            "tickets:read:all" in user_permissions):
        raise HTTPException(status_code=403, detail="Not authorized to view this ticket")
        
    return db_ticket

@router.post(
    "/{ticket_id}/replies", 
    response_model=schemas.TicketReply,
    status_code=status.HTTP_201_CREATED
)
def create_ticket_reply(
    ticket_id: int,
    reply: schemas.TicketReplyCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user_from_token)
):
    """
    Adds a new reply to an existing ticket.
    """
    # First, run the same security check as read_ticket_details to ensure user can access this ticket
    read_ticket_details(ticket_id, db, current_user)

    db_reply = models.TicketReply(
        message=reply.message,
        ticket_id=ticket_id,
        user_id=current_user.id
    )
    db.add(db_reply)
    db.commit()
    db.refresh(db_reply)

    # Also update the 'updated_at' timestamp of the parent ticket
    db.query(models.Ticket).filter(models.Ticket.id == ticket_id).update({'updated_at': func.now()})
    db.commit()
    
    # Here you would trigger a Push Notification to the other party
    # send_notification_for_ticket_reply(db, ticket_id, current_user.id)
    
    return db_reply
