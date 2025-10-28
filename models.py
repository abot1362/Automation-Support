# models.py - نسخه نهایی DashboardWidget

class DashboardWidget(Base):
    """ذخیره تنظیمات ویجت‌های سفارشی برای هر کاربر (ادمین یا کاربر نهایی)"""
    __tablename__ = 'dashboard_widgets'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    
    # نوع ویجت، مثلا: 'live_traffic', 'cpu_status', 'user_internet_usage'
    widget_type = Column(String(100), nullable=False) 
    
    # تنظیمات ویجت به صورت JSON (مثلاً ID دستگاه یا اینترفیس مورد نظر)
    widget_config_json = Column(Text) 
    
    # اطلاعات موقعیت و اندازه در گرید
    position_x = Column(Integer, nullable=False)
    position_y = Column(Integer, nullable=False)
    width = Column(Integer, nullable=False)
    height = Column(Integer, nullable=False)
    
    user = relationship("User")
