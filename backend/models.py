# backend/models.py (نسخه نهایی با پشتیبانی از کاربران خارجی)

# ... (سایر import ها و مدل‌ها) ...

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=True)
    
    # برای کاربران محلی، این فیلد پر می‌شود. برای کاربران خارجی، NULL است.
    hashed_password = Column(String(255), nullable=True) 
    
    full_name = Column(String(100), nullable=True)
    is_active = Column(Boolean, default=True)
    role_id = Column(Integer, ForeignKey('roles.id'))
    user_type = Column(Enum('admin', 'end_user', name='user_type_enum'), default='end_user', nullable=False)
    
    # --- فیلدهای جدید برای یکپارچه‌سازی ---
    # منبع احراز هویت کاربر (محلی، ldap, kerberos)
    auth_source = Column(String(50), default='local', nullable=False) 
    # شناسه منحصر به فرد کاربر در سیستم خارجی (مثلاً objectGUID در AD)
    external_id = Column(String(255), nullable=True, index=True) 

    role = relationship("Role", back_populates="users", lazy="joined")
