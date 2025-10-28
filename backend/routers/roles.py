# backend/routers/roles.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models, schemas, database
from dependencies import require_permission

router = APIRouter(
    prefix="/api/administration/roles",
    tags=["RBAC - Roles & Permissions"],
    dependencies=[Depends(require_permission("administration:roles:read"))]
)

@router.get("/", response_model=List[schemas.Role])
def get_all_roles(db: Session = Depends(database.get_db)):
    """Lists all available roles in the system."""
    return db.query(models.Role).all()

@router.post("/", response_model=schemas.Role, dependencies=[Depends(require_permission("administration:roles:create"))])
def create_role(role: schemas.RoleCreate, db: Session = Depends(database.get_db)):
    """Creates a new role."""
    db_role = models.Role(name=role.name, description=role.description)
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role

@router.get("/{role_id}/permissions", response_model=List[schemas.Permission])
def get_role_permissions(role_id: int, db: Session = Depends(database.get_db)):
    """Gets all permissions assigned to a specific role."""
    role = db.query(models.Role).filter(models.Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return [p.permission for p in role.permissions]

@router.put("/{role_id}/permissions", dependencies=[Depends(require_permission("administration:roles:assign_permissions"))])
def update_role_permissions(role_id: int, permission_ids: List[int], db: Session = Depends(database.get_db)):
    """Updates the set of permissions for a specific role."""
    role = db.query(models.Role).filter(models.Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
        
    # Clear existing permissions for this role
    db.query(models.RolePermission).filter(models.RolePermission.role_id == role_id).delete()
    
    # Add the new permissions
    for p_id in permission_ids:
        db.add(models.RolePermission(role_id=role_id, permission_id=p_id))
        
    db.commit()
    return {"status": "success"}

# --- Permissions Endpoint ---
@router.get("/all-permissions", response_model=List[schemas.Permission], dependencies=[Depends(require_permission("administration:roles:read"))])
def get_all_system_permissions(db: Session = Depends(database.get_db)):
    """Lists all possible permissions defined in the system."""
    return db.query(models.Permission).order_by(models.Permission.name).all()
