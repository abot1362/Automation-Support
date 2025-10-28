# backend/routers/webfilter.py

from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
import models, database
from security import get_current_user
from dependencies import require_permission

router = APIRouter(
    prefix="/api/webfilter",
    tags=["Web Filter"],
    dependencies=[Depends(require_permission("webfilter:manage"))]
)

# --- CRUD for Filter Profiles, Categories, Sources ---
# ... (Full CRUD endpoints for managing these in the database)

@router.get("/profiles")
def get_filter_profiles(db: Session = Depends(database.get_db)):
    return db.query(models.WebFilterProfile).all()

# --- Public Endpoint for MikroTik to download the blacklist ---
@router.get(
    "/export/blacklist/{profile_id}.txt",
    response_class=Response,
    dependencies=[] # No auth required for this specific endpoint
)
def export_blacklist_for_mikrotik(profile_id: int, db: Session = Depends(database.get_db)):
    """
    Generates a plain text file of all domains to be blocked for a given profile.
    This is the URL the MikroTik script will fetch.
    """
    profile = db.query(models.WebFilterProfile).filter(models.WebFilterProfile.id == profile_id).first()
    if not profile:
        return Response(content="Profile not found.", status_code=404)

    # Get all categories linked to this profile
    linked_categories = [link.category_id for link in profile.categories] # Assuming relationship is defined in model

    # Get all blacklist entries from those categories
    entries = db.query(models.BlacklistEntry.entry).filter(
        models.BlacklistEntry.category_id.in_(linked_categories)
    ).all()

    content = "\n".join([entry[0] for entry in entries])
    
    return Response(content=content, media_type="text/plain")
