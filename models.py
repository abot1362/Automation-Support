from sqlalchemy import (
    Column, Integer, String, Boolean, ForeignKey, Text, Enum, 
    TIMESTAMP, Float, BigInteger
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base # Import Base from database.py

# --- RBAC, Admin, and Auditing ---
class Role(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    permissions = relationship("RolePermission", back_populates="role", cascade="all, delete-orphan")
    users = relationship("User", back_populates="role")

class Permission(Base):
    __tablename__ = 'permissions'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)

class RolePermission(Base):
    __tablename__ = 'role_permissions'
    role_id = Column(Integer, ForeignKey('roles.id', ondelete='CASCADE'), primary_key=True)
    permission_id = Column(Integer, ForeignKey('permissions.id', ondelete='CASCADE'), primary_key=True)
    role = relationship("Role", back_populates="permissions")

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role_id = Column(Integer, ForeignKey('roles.id'))
    user_type = Column(Enum('admin', 'end_user', name='user_type_enum'), default='end_user', nullable=False)
    role = relationship("Role", back_populates="users")

# ... (Add all other models as defined in previous detailed answers)
