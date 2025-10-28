from sqlalchemy import (
    Column, Integer, String, Boolean, ForeignKey, Text, Enum, 
    TIMESTAMP, Float, BigInteger
)
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

# --- بخش ۱: مدیریت کاربران، نقش‌ها و دسترسی‌ها (RBAC) ---

class Role(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    
    permissions = relationship("RolePermission", back_populates="role", cascade="all, delete-orphan")
    users = relationship("User", back_populates="role")

class Permission(Base):
    __tablename__ = 'permissions'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=True)

class RolePermission(Base):
    __tablename__ = 'role_permissions'
    role_id = Column(Integer, ForeignKey('roles.id', ondelete='CASCADE'), primary_key=True)
    permission_id = Column(Integer, ForeignKey('permissions.id', ondelete='CASCADE'), primary_key=True)
    role = relationship("Role", back_populates="permissions")

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=True)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=True)
    is_active = Column(Boolean, default=True)
    role_id = Column(Integer, ForeignKey('roles.id'))
    user_type = Column(Enum('admin', 'end_user', name='user_type_enum'), default='end_user', nullable=False)
    
    role = relationship("Role", back_populates="users")
    
# --- بخش ۲: مدیریت دستگاه‌ها (چند-بُره‌ای) ---

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

class UniFiController(Base): __tablename__ = 'unifi_controllers'; id = Column(Integer, primary_key=True); #... (Full schema)
class FortiGateDevice(Base): __tablename__ = 'fortigate_devices'; id = Column(Integer, primary_key=True); #... (Full schema)
class VMwareVCenter(Base): __tablename__ = 'vmware_vcenters'; id = Column(Integer, primary_key=True); #... (Full schema)
class ProxmoxServer(Base): __tablename__ = 'proxmox_servers'; id = Column(Integer, primary_key=True); #... (Full schema)
class DockerHost(Base): __tablename__ = 'docker_hosts'; id = Column(Integer, primary_key=True); #... (Full schema)

# --- بخش ۳: ارتباطات و نظارت تصویری ---

class FreeSwitchServer(Base): __tablename__ = 'freeswitch_servers'; id = Column(Integer, primary_key=True); #... (Full schema)
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

class ChatRoom(Base): __tablename__ = 'chat_rooms'; id = Column(Integer, primary_key=True); #... (Full schema)
class ChatMessage(Base): __tablename__ = 'chat_messages'; id = Column(Integer, primary_key=True); #... (Full schema)

# --- بخش ۴: تحلیل، گزارش‌دهی و مدیریت سیستم ---

class AuditLog(Base): __tablename__ = 'audit_logs'; id = Column(Integer, primary_key=True); #... (Full schema)
class DeviceInventory(Base): __tablename__ = 'device_inventory'; id = Column(Integer, primary_key=True); #... (Full schema)
class TopologyLink(Base): __tablename__ = 'topology_links'; id = Column(Integer, primary_key=True); #... (Full schema)
class AlertRule(Base): __tablename__ = 'alert_rules'; id = Column(Integer, primary_key=True); #... (Full schema)
class ComplianceRule(Base): __tablename__ = 'compliance_rules'; id = Column(Integer, primary_key=True); #... (Full schema)
class BackupJob(Base): __tablename__ = 'backup_jobs'; id = Column(Integer, primary_key=True); #... (Full schema)

# --- بخش ۵:
