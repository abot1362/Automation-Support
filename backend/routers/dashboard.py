# routers/dashboard.py

@router.get("/my-widgets")
def get_my_dashboard_widgets(current_user: models.User = Depends(get_current_user), db: Session = Depends(database.get_db)):
    """تنظیمات ویجت‌های داشبورد کاربر فعلی را برمی‌گرداند."""
    return db.query(models.DashboardWidget).filter(models.DashboardWidget.user_id == current_user.id).all()

@router.post("/my-widgets/save-layout")
def save_dashboard_layout(layout_data: List[schemas.WidgetLayout], current_user: models.User = Depends(get_current_user), db: Session = Depends(database.get_db)):
    """چیدمان جدید ویجت‌ها را ذخیره می‌کند."""
    # ۱. تمام ویجت‌های قدیمی کاربر را حذف کن
    db.query(models.DashboardWidget).filter(models.DashboardWidget.user_id == current_user.id).delete()
    # ۲. ویجت‌های جدید را با موقعیت جدید اضافه کن
    for widget_info in layout_data:
        new_widget = models.DashboardWidget(user_id=current_user.id, **widget_info.dict())
        db.add(new_widget)
    db.commit()
    return {"status": "success"}
