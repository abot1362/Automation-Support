# backend/routers/monitoring.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
import models, database, schemas
from security import get_current_user_from_token
from dependencies import require_permission

router = APIRouter(
    prefix="/api/monitoring",
    tags=["Monitoring"],
    dependencies=[Depends(require_permission("monitoring:read"))]
)

@router.get("/users/{username}/usage")
def get_user_internet_usage(
    device_id: int,
    username: str, 
    start_date: datetime, 
    end_date: datetime,
    db: Session = Depends(database.get_db)
):
    """
    Retrieves historical internet usage for a specific user on a specific device.
    This data should be collected periodically by a background job from MikroTik's accounting.
    For this example, we'll query the UserInternetUsage table.
    """
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    # Query to aggregate daily usage from the UserInternetUsage table
    usage_data = db.query(
        func.date(models.UserInternetUsage.timestamp).label("date"),
        func.sum(models.UserInternetUsage.upload_bytes).label("total_upload"),
        func.sum(models.UserInternetUsage.download_bytes).label("total_download")
    ).filter(
        models.UserInternetUsage.user_id == user.id,
        models.UserInternetUsage.timestamp.between(start_date, end_date)
    ).group_by(func.date(models.UserInternetUsage.timestamp)).order_by("date").all()
    
    return usage_data
