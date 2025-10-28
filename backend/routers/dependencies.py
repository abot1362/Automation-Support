
# backend/dependencies.py

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from security import get_current_user_from_token # Assumes this function returns the full User object
import models
import database

def require_permission(required_permission: str):
    """
    A FastAPI dependency that checks if the current user has the required permission.
    This is the core of the RBAC enforcement.
    """
    async def permission_checker(
        current_user: models.User = Depends(get_current_user_from_token)
    ):
        if not current_user or not current_user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated or inactive user",
            )
        
        # Super Admins have god mode :)
        if current_user.role and current_user.role.name == "Super Admin":
            return current_user # Grant access immediately

        # Extract permission names from the user's role
        user_permissions = {p.permission.name for p in current_user.role.permissions}

        if required_permission not in user_permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permission denied. Requires: '{required_permission}'",
            )
        
        return current_user
        
    return permission_checker
