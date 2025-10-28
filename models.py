# backend/models.py

from sqlalchemy import (Column, Integer, String, Boolean, ForeignKey, Text)
from sqlalchemy.orm import relationship
from database import Base # Import Base from your database.py

# --- RBAC Models ---

class Role(Base):
    """Defines a role, which is a collection of permissions (e.g., 'Admin', 'Viewer')."""
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)
    
    # A role can be assigned to many users
    users = relationship("User", back_populates="role")
    # A role has many permissions, accessed through the association table
    permissions = relationship("RolePermission", back_populates="role", cascade="all, delete-orphan")

class Permission(Base):
    """Defines a single, granular permission in the system (e.g., 'devices:create')."""
    __tablename__ = 'permissions'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)

class RolePermission(Base):
    """Association table to link Roles with Permissions (many-to-many)."""
    __tablename__ = 'role_permissions'
    role_id = Column(Integer, ForeignKey('roles.id', ondelete='CASCADE'), primary_key=True)
    permission_id = Column(Integer, ForeignKey('permissions.id', ondelete='CASCADE'), primary_key=True)
    
    role = relationship("Role", back_populates="permissions")
    permission = relationship("Permission")

class User(Base):
    """Defines a user of the platform."""
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role_id = Column(Integer, ForeignKey('roles.id'))
    is_active = Column(Boolean, default=True)
    user_type = Column(Enum('admin', 'end_user', name='user_type_enum'), default='end_user', nullable=False)
    
    # A user has one role
    role = relationship("Role", back_populates="users", lazy="joined") # lazy="joined" is crucial for performance```
**نکته مهم:** `lazy="joined"` در رابطه `User.role` به SQLAlchemy می‌گوید که هنگام خواندن یک کاربر، اطلاعات نقش او را نیز به صورت خودکار با یک `JOIN` دریافت کند. این کار عملکرد را به شدت بهبود می‌بخشد.

**اقدام بعدی:** پس از به‌روزرسانی این فایل، دستورات Alembic را اجرا کنید:
```bash
alembic revision --autogenerate -m "Finalize RBAC models and relationships"
alembic upgrade head
