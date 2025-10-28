from sqlalchemy import (Column, Integer, String, Boolean, ForeignKey, Text, Enum, TIMESTAMP, Float, BigInteger)
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

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

class AuditLog(Base):
    __tablename__ = 'audit_logs'
    id = Column(Integer, primary_key=True)
    # ... (full schema as designed before)

# --- Device Management (Generic & Specific) ---
class Device(Base):
    __tablename__ = 'devices'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    vendor = Column(String(50), nullable=False)
    os_type = Column(String(50), nullable=True)
    management_protocol = Column(String(50), nullable=False)
    host = Column(String(100), nullable=False)
    port = Column(Integer, nullable=True)
    username = Column(String(100), nullable=False)
    password = Column(String(255), nullable=False) # Encrypted
    is_active = Column(Boolean, default=True)

class VMwareVCenter(Base): __tablename__ = 'vmware_vcenters'; id = Column(Integer, primary_key=True); name=Column(String(100)); #...
class ProxmoxServer(Base): __tablename__ = 'proxmox_servers'; id = Column(Integer, primary_key=True); name=Column(String(100)); #...
class DockerHost(Base): __tablename__ = 'docker_hosts'; id = Column(Integer, primary_key=True); name=Column(String(100)); #...
class FortiGateDevice(Base): __tablename__ = 'fortigate_devices'; id = Column(Integer, primary_key=True); name=Column(String(100)); #...
class UniFiController(Base): __tablename__ = 'unifi_controllers'; id = Column(Integer, primary_key=True); name=Column(String(100)); #...

class SurveillanceSystem(Base):
    __tablename__ = 'surveillance_systems'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    system_type = Column(Enum('Hikvision', 'Dahua', 'Shinobi', 'ZoneMinder', name='surv_system_type_enum'), nullable=False)
    host = Column(String(100), nullable=False)
    port = Column(Integer, nullable=False)
    username = Column(String(100), nullable=False)
    password = Column(String(255), nullable=False)
    api_key = Column(String(255), nullable=True)
    group_id = Column(String(100), nullable=True)

# ... Placeholder for other models like Chat, Tickets, Alerts, etc.
