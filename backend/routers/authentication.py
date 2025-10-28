from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta
import ldap # برای LDAP Bind

# ... (سایر import ها)
from security import verify_password, create_access_token
# from kerberos_auth import kerberos_auth # یک dependency جدید برای Kerberos

router = APIRouter(
    tags=["Authentication"]
)

# فرض می‌کنیم تنظیمات از دیتابیس خوانده شده‌اند
LDAP_SERVER = "ldap://dc.mycorp.local"
LDAP_BASE_DN = "ou=Users,dc=mycorp,dc=local"

@router.post("/token")
async def login_for_access_token(
    form_data: dict, # دیگر از OAuth2PasswordRequestForm استفاده نمی‌کنیم
    db: Session = Depends(database.get_db)
):
    """
    Handles login for multiple authentication providers.
    """
    username = form_data.get("username")
    password = form_data.get("password")
    auth_type = form_data.get("type", "local") # 'local' or 'ldap'

    user = None
    
    if auth_type == "local":
        user = db.query(models.User).filter(models.User.username == username, models.User.auth_source == 'local').first()
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")

    elif auth_type == "ldap":
        try:
            # تلاش برای اتصال (Bind) به سرور LDAP با اطلاعات کاربر
            con = ldap.initialize(LDAP_SERVER)
            con.protocol_version = ldap.VERSION3
            # ساختن distinguished name (DN) کاربر
            user_dn = f"cn={username},{LDAP_BASE_DN}"
            con.simple_bind_s(user_dn, password)
            
            # اگر bind موفق بود، کاربر را در دیتابیس خودمان پیدا یا ایجاد می‌کنیم
            user = db.query(models.User).filter(models.User.username == username, models.User.auth_source == 'ldap').first()
            if not user:
                # اگر کاربر وجود نداشت، او را همگام‌سازی می‌کنیم (این یک پیاده‌سازی ساده شده است)
                # در دنیای واقعی، یک جاب همگام‌سازی جداگانه این کار را انجام می‌دهد
                # new_user = models.User(username=username, auth_source='ldap', role_id=default_role_id)
                # db.add(new_user); db.commit(); db.refresh(new_user)
                # user = new_user
                raise HTTPException(status_code=404, detail="User not found in local database. Please sync users first.")

            con.unbind_s()
        except ldap.INVALID_CREDENTIALS:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect LDAP username or password")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"LDAP connection error: {e}")

    if not user:
        raise HTTPException(status_code=401, detail="Authentication failed.")

    # صدور توکن JWT
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

# Endpoint برای Kerberos SSO
# @router.get("/sso/kerberos", dependencies=[Depends(kerberos_auth)])
# async def kerberos_sso_login(
#     user_principal: str = Depends(kerberos_auth),
#     db: Session = Depends(database.get_db)
# ):
#     # user_principal از dependency کربروس می‌آید (مثلاً: user@MYCORP.LOCAL)
#     username = user_principal.split('@')[0]
#     user = db.query(models.User).filter(models.User.username == username).first()
#     # ... (منطق صدور توکن برای کاربر SSO)
