from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

# In a full production app, you would import and include all your API routers.
# This keeps the main file clean.
# Example:
# from routers import devices, surveillance, users, notifications
# from config import settings

app = FastAPI(
    title="Unified Infrastructure Management Platform",
    description="A central dashboard for managing multi-vendor network and infrastructure devices.",
    version="1.0.0"
)

# --- Include API Routers ---
# app.include_router(devices.router, prefix="/api", tags=["Devices"])
# app.include_router(notifications.router, prefix="/api/notifications", tags=["Notifications"])
# ... and so on for all other routers

@app.get("/api/health", tags=["System"])
def health_check():
    """Provides a simple health check endpoint."""
    return {"status": "ok"}

# --- Serve Frontend PWA Files ---
# In a production environment, this is best handled by Nginx.
# These lines are provided for local development and testing convenience.
app.mount("/portal", StaticFiles(directory="user_portal_public", html=True), name="user_portal")
app.mount("/", StaticFiles(directory="public", html=True), name="admin_portal")
