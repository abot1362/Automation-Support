from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from database import engine
import models

# In a full production app, you would import and include all your API routers.
# This is a simplified version for structure.
# from routers import devices, surveillance, users, notifications, etc.

# This command is helpful for initial setup if not using Alembic,
# but Alembic is the recommended approach for production.
# models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Unified Infrastructure Management Platform",
    description="A central dashboard for managing multi-vendor network and infrastructure devices.",
    version="1.0.0"
)

# --- Include API Routers Here ---
# Example:
# app.include_router(devices.router, prefix="/api", tags=["Devices"])
# app.include_router(notifications.router, prefix="/api/notifications", tags=["Notifications"])
# ... and so on for all other routers

@app.get("/api/health", tags=["System"])
def health_check():
    """Provides a simple health check endpoint to confirm the API is running."""
    return {"status": "ok", "message": "Backend is running!"}

# --- Serve Frontend Files ---
# In a production environment, this is best handled by a dedicated web server like Nginx.
# These lines are provided for local development and testing convenience.
app.mount("/portal", StaticFiles(directory="user_portal_public", html=True), name="user_portal")
app.mount("/", StaticFiles(directory="public", html=True), name="admin_portal")

# Example of a startup event to load background jobs
@app.on_event("startup")
async def startup_event():
    print("Application startup complete. Loading background jobs...")
    # Here you would start your APScheduler with jobs for backups, alerting, etc.
